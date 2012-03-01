#!/usr/bin/env python
import json
import functools
import time
import tornado.web
from pymongo.objectid import ObjectId
from periscope.handlers import NetworkResourceHandler
from periscope.handlers import SSEHandler
from periscope.test.base import PeriscopeHTTPTestCase

MIME = {
    'HTML': 'text/html',
    'JSON': 'application/json',
    'PLAIN': 'text/plain',
    'SSE': 'text/event-stream',
    'PSJSON': 'application/perfsonar+json',
    'PSXML': 'application/perfsonar+xml',
}


class SSEHandlerTest(PeriscopeHTTPTestCase):
    def get_app(self):
        class SimpleSSEHandler(SSEHandler):
            def _write_callback(self):
                self.write_event("id1", "message", "data 1\ndata 2")
                self.finish()

            @tornado.web.asynchronous
            def get(self):
                if self.supports_sse():
                    self.write_event("id0", "message", "data 0")
                    self._write_callback()
                else:
                    self.set_header("Content-Type", self.request.headers.get("Accept"))
                    self.write("None SSE Request")
                    self.finish()

        return tornado.web.Application([("/sse", SimpleSSEHandler)])

    def test_stream(self):
        def stream_callback(response):
            self.assertEqual(response.code, 200)
            self.assertEqual(response.headers.get("Content-Type", None), MIME['SSE'])
            self.assertEqual(response.headers.get("Transfer-Encoding", None), "chunked")
            self.assertEqual(response.headers.get("Cache-Control", None), "no-cache")
            body_lines = response.body.split("\n")
            self.assertEqual(body_lines[0], "retry:%d" % SSEHandler.DEFAULT_RETRY)
            self.assertEqual(body_lines[1], "")
            self.assertEqual(body_lines[2], "id:id0")
            self.assertEqual(body_lines[3], "event:message")
            self.assertEqual(body_lines[4], "data:data 0")
            self.assertEqual(body_lines[5], "")
            self.assertEqual(body_lines[6], "id:id1")
            self.assertEqual(body_lines[7], "event:message")
            self.assertEqual(body_lines[8], "data:data 1")
            self.assertEqual(body_lines[9], "data:data 2")
            self.assertEqual(body_lines[10], "")
            self.assertEqual(body_lines[11], "")
            self.stop()

        self.http_client.fetch(self.get_url("/sse"),
                            stream_callback,
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['SSE'],
                                "Connection": "close",})
        self.wait()

    def test_normal_get(self):
        def get_callback(response):
            self.assertEqual(response.code, 200)
            self.assertEqual(response.headers.get("Content-Type"), MIME['PLAIN'])
            body_lines = response.body.split("\n")
            self.assertEqual(body_lines[0], "None SSE Request")
            self.stop()
        
        self.http_client.fetch(self.get_url("/sse"),
                            get_callback,
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PLAIN'],
                                "Connection": "close",})
        self.wait()


class NetworkResourceHandlerTest(PeriscopeHTTPTestCase):
    # TODO: Need DBLayer Mock to isolate NetworkResourceHandler testing.
    def __init__(self, *args, **kwargs):
        super(NetworkResourceHandlerTest, self).__init__(*args, **kwargs)
        self.collection_name = "test_res_handler"

    def setUp(self):
        super(NetworkResourceHandlerTest, self).setUp()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)
        self.sync_db.create_collection(self.collection_name, capped=True, size=100)

    def tearDown(self):
        super(NetworkResourceHandlerTest, self).tearDown()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)

    def get_app(self):
        async_db = self.async_db
        class NetworkResourceApp(tornado.web.Application):
            @property
            def async_db(self):
                return async_db

        return NetworkResourceApp([
                    ("/nodes", NetworkResourceHandler, dict(collection_name=self.collection_name, base_url="/nodes")),
                    ("/nodes/(?P<res_id>[^\/]+)", NetworkResourceHandler, dict(collection_name="test_res_handler", base_url="/nodes")),
                    (r'/nodes/(?P<res_id>[^\/]+)(?P<kwpath>/.*)?$', NetworkResourceHandler, dict(collection_name="test_res_handler", base_url="/nodes")),
                    ("/topologies", NetworkResourceHandler, dict(collection_name="topologies", base_url="/nodes")),
                ])

    def _create_node(self, nodeid):
        node = {
            "$schema": "http://example.org/20110401/unis/node#",            
            "description": "This is a test network resource",
            "names": {
                "hostname": [nodeid, "some_other_name"]
            },
            "lifetime": {
                "start": "11-12-1990 11:13:56",
                "end": "11-12-2020 11:13:56"
            },
            "location": {
                "institution": "Indiana University"
            },
            "operating_system": {
                "name": "Linux"
            },
            "events": {
                "errors": "http://localhost:8888/events/2",
                "utilization": "http://localhost:8888/events/1"
            }
        }
        return node
        
    def _insert_nodes(self, num=5):
        """Creates sample Nodes and insert them to MongoDB"""
        nodes = []
        for i in range(num):
            node = self._create_node("node_%d" % i)
            node["id"] = str(ObjectId())
            node["\\$schema"] = node["$schema"]
            del node["$schema"]
            self.sync_db[self.collection_name].insert(node)
            node.pop('_id', None)
            node["$schema"] = node["\\$schema"]
            del node["\\$schema"]
            nodes.append(node)
        return nodes
    
    def test_get_individual(self):
        """Test retrieving each node"""
        nodes = self._insert_nodes(5)
        for node in nodes:
            response = self.fetch("/nodes/" + node['id'],
                    headers={"Accept": MIME['PSJSON'], "Connection": "close"})
            self.assertEqual(response.code, 200)
            self.assertEqual(node, json.loads(response.body))

    def test_get_list(self):
        """Test retrieving list of nodes"""
        nodes = self._insert_nodes(5)
        response = self.fetch("/nodes",
                    headers={"Accept": MIME['PSJSON'], "Connection": "close"})
        self.assertEqual(response.code, 200)
        ret_nodes = json.loads(response.body)
        self.assertEqual(len(nodes), len(ret_nodes))
        for node in nodes:
            self.assertIn(node, ret_nodes)

    def test_get_404(self):
        # Test node does not exist
        response = self.fetch("/nodes/YYYY",
                headers={"Accept": MIME['PSJSON'], "Connection": "close"})
        self.assertEqual(response.code, 404)

    def test_stream(self):
        # TODO: This test is incomplete because it doesn't actually validate
        #       the returned output
        self._insert_nodes(5)
        def get_callback(response):
            self.assertEqual(response.code, 599)
            self.stop()

        def streaming_callback(response):
            self.assertIsInstance(json.loads(response), list)

        def _insert_callback(res_id):
            node = {"id": res_id, "urn": "node%s" % res_id}
            self.sync_db[self.collection_name].insert(node)

        for i in range(5):
            insert_callback = functools.partial(_insert_callback, i + 5)
            self.io_loop.add_timeout(time.time() + i, insert_callback)

        self.http_client.fetch(self.get_url("/nodes"),
                            get_callback,
                            streaming_callback=streaming_callback,
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "keep-alive"},
                            request_timeout=6)
        self.wait(timeout=10)

    def test_stream_multiple_clients(self):
        # TODO: This test is incomplete because it doesn't actually validate
        #       the returned output
        self._insert_nodes(5)
        def get_callback(response):
            self.assertEqual(response.code, 599)
            self.stop()

        def streaming_callback(response):
            self.assertIsInstance(json.loads(response), list)
        
        def _insert_callback(res_id):
            node = {"id": res_id, "urn": "node%s" % res_id}
            self.sync_db[self.collection_name].insert(node)
        
        for i in range(5):
            insert_callback = functools.partial(_insert_callback, i + 5)
            self.io_loop.add_timeout(time.time() + i, insert_callback)

        for i in range(10):
            self.http_client.fetch(self.get_url("/nodes"),
                                get_callback,
                                streaming_callback=streaming_callback,
                                headers={"Cache-Control": "no-cache",
                                    "Accept": MIME['PSJSON'],
                                    "Connection": "keep-alive"},
                                request_timeout=6)
        self.wait(timeout=10)

    def test_post(self):
        def post_callback(response, expected):
            self.assertEqual(response.code, 202)
            res_id = unicode(response.headers['Location'].split('/')[-1])
            result = self.sync_db[self.collection_name].find_one({'id': res_id})
            # Unescape special chars
            result = json.loads(json.dumps(result).replace("\\\\$", "$"))
            expected['id'] = res_id
            self.assertEqual(result, expected)
            self.stop()

        node = self._create_node("node_test")
        callback = functools.partial(post_callback, expected=node)
        self.http_client.fetch(self.get_url("/nodes"),
                            callback,
                            method="POST",
                            body=json.dumps(node), 
                            headers={
                                "Content-Type": MIME['PSJSON'],
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"},
                            request_timeout=6)
        self.wait()
    
    def test_post_get(self):
        node = self._create_node("node_test")
        post_response = self.fetch("/nodes",
                            method="POST",
                            body=json.dumps(node), 
                            headers={
                                "Content-Type": MIME['PSJSON'],
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
    
        res_id = unicode(post_response.headers['Location'].split('/')[-1])
        node['id'] = res_id
        get_response = self.fetch("/nodes/%s" % res_id,
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        
        ret_node = json.loads(get_response.body)
        self.assertEqual(node, ret_node)
    
    def test_post_get_subpath(self):
        node = self._create_node("node_test")
        post_response = self.fetch("/nodes",
                            method="POST",
                            body=json.dumps(node), 
                            headers={
                                "Content-Type": MIME['PSJSON'],
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
    
        res_id = unicode(post_response.headers['Location'].split('/')[-1])
        # Events
        get_events = self.fetch("/nodes/%s/events/" % res_id,
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        ret_events = json.loads(get_events.body)
        self.assertEqual(node['events'], ret_events)
        
        for event in node['events']:
            get_event = self.fetch("/nodes/%s/events/%s" % (res_id, event),
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
            self.assertEqual(node['events'][event], get_event.body.strip("\""))
        
        # Names
        get_names = self.fetch("/nodes/%s/names/" % res_id,
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        ret_names = json.loads(get_names.body)
        self.assertEqual(node['names'], ret_names)
        
        for name in node['names']:
            get_names = self.fetch("/nodes/%s/names/%s" % (res_id, name),
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
            ret_names = json.loads(get_names.body)
            self.assertEqual(node['names'][name], ret_names)
            
            for index in range(len(node['names'][name])):
                get_name = self.fetch("/nodes/%s/names/%s/%d" % (res_id, name, index),
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
                ret_name = get_name.body.strip("\"")
                self.assertEqual(node['names'][name][index], ret_name)                                                
