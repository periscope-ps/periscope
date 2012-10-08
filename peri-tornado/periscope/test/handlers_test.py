#!/usr/bin/env python
import copy
import json
import functools
import time
import tornado.web
from mock import Mock
from mock import patch
from tornado.httpclient import HTTPError
from tornado.httpserver import HTTPRequest
import pymongo
if pymongo.version_tuple[1] > 1:
    from bson.objectid import ObjectId
else:
    from pymongo.objectid import ObjectId

from periscope.db import DBLayer
from periscope.db import dumps_mongo
from periscope.utils import load_class
from periscope.handlers import CollectionHandler
from periscope.handlers import NetworkResourceHandler
from periscope.handlers import SSEHandler
from periscope.models import Topology
from periscope.models import Node
from periscope.models import schemaLoader
from periscope.test.base import PeriscopeHTTPTestCase

MIME = {
    'HTML': 'text/html',
    'JSON': 'application/json',
    'PLAIN': 'text/plain',
    'SSE': 'text/event-stream',
    'PSJSON': 'application/perfsonar+json',
    'PSXML': 'application/perfsonar+xml',
    }

schemas = {
    'networkresource': 'http://unis.incntre.iu.edu/schema/20120709/networkresource#',
    'node': 'http://unis.incntre.iu.edu/schema/20120709/node#',
    'port': 'http://unis.incntre.iu.edu/schema/20120709/port#',
    'link': 'http://unis.incntre.iu.edu/schema/20120709/link#',
    'service': 'http://unis.incntre.iu.edu/schema/20120709/service#',
    'domain': 'http://unis.incntre.iu.edu/schema/20120709/domain#',
    'topology': 'http://unis.incntre.iu.edu/schema/20120709/topology#',
}

class SSEHandlerTest(PeriscopeHTTPTestCase):
    def get_app(self):
        class SimpleSSEHandler(SSEHandler):
            def _write_callback(self):
                self.write_event("id1", "message", "data 1\ndata 2")
                self.finish()

            #@tornado.web.asynchronous
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


class NetworkResourceHandlerIntegrationTest(PeriscopeHTTPTestCase):
    def __init__(self, *args, **kwargs):
        super(NetworkResourceHandlerIntegrationTest, self).__init__(*args, **kwargs)
        self.collection_name = "test_res_handler"

    def setUp(self):
        super(NetworkResourceHandlerIntegrationTest, self).setUp()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)
        self.sync_db.create_collection(self.collection_name, capped=True, size=100)

    def tearDown(self):
        super(NetworkResourceHandlerIntegrationTest, self).tearDown()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)

    def _create_node(self, nodeid):
        node = {
            u"$schema": unicode(schemas['node']),
            u"description": u"This is a test network resource",
            u"name": unicode(nodeid),
            u"lifetimes": [
                {
                    u"start": u"2012-03-01T13:00:00Z",
                    u"end": u"2012-03-01T13:00:00Z"
                }
            ],
            u"location": {
                u"institution": u"Indiana University"
            }
        }
        return node
        
    def _insert_nodes(self, num=5):
        """Creates sample Nodes and insert them to MongoDB"""
        nodes = []
        for i in range(num):
            node = self._create_node("node_%d" % i)
            node["id"] = str(ObjectId())
            node["\\$schema"] = node.pop("$schema")
            self.sync_db[self.collection_name].insert(node)
            node.pop('_id', None)
            node["$schema"] = node.pop("\\$schema")
            nodes.append(node)
        return nodes
    
    def test_get_individual(self):
        """Test retrieving each node"""
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        nodes = self._insert_nodes(5)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=False)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/nodes/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])

        # Act
        responses = []
        for node in nodes:
            response = self.fetch("/nodes/" + node['id'],
                    headers={"Accept": MIME['PSJSON'], "Connection": "keep-alive"})
            responses.append(response)

        # Assert
        self.assertEqual(len(responses), len(nodes))
        for i in range(len(nodes)):
            node = nodes[i]
            response = responses[i]
            self.assertEqual(response.code, 200)
            self.assertEqual(node, json.loads(response.body))

    def test_get_list(self):
        """Test retrieving list of nodes"""
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        nodes = self._insert_nodes(5)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['node']
        handler = ("/nodes$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        schemas_single={MIME['PSJSON']: schemas['node']}))
        self._app.add_handlers(".*$", [handler])
        
        # Act
        response = self.fetch("/nodes",
                    headers={"Accept": MIME['PSJSON'],
                    "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 200)
        ret_nodes = json.loads(response.body)
        self.assertEqual(len(nodes), len(ret_nodes))
        
        # TODO (AH): This need to be re-done such only hrefs are returned
        for node in nodes:
            self.assertIn(node, ret_nodes)

    def test_get_404(self):
        # Test node does not exist
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/nodes/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        
        # Act
        response = self.fetch("/nodes/YYYY",
                headers={"Accept": MIME['PSJSON'], "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 404)
    """
    def test_stream(self):
        # TODO: This test is incomplete because it doesn't actually validate
        #       the returned output
        
        # Arrange
        self._insert_nodes(5)
        self.sync_db[self.collection_name].create_index([("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/nodes$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        
        def get_callback(response):
            self.assertEqual(response.code, 599)
            self.stop()

        def streaming_callback(response):
            self.assertIsInstance(json.loads(response), list)

        def _insert_callback(res_id):
            node = {"id": res_id, "ts": int(time.time() * 1000000)}
            self.sync_db[self.collection_name].insert(node)

        for i in range(5):
            insert_callback = functools.partial(_insert_callback, i + 5)
            self.io_loop.add_timeout(time.time() + i, insert_callback)
        
        # Act
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
        self.sync_db[self.collection_name].create_index([("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/nodes$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        
        def get_callback(response):
            self.assertEqual(response.code, 599)
            self.stop()

        def streaming_callback(response):
            self.assertIsInstance(json.loads(response), list)
        
        def _insert_callback(res_id):
            node = {"id": res_id, "ts": int(time.time() * 1000000)}
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
    """    
    def test_post(self):
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        node = self._create_node("node_test")
        content_type = MIME['PSJSON'] + '; profile=' + schemas['node']
        handler = ("/nodes$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['node']}))
        self._app.add_handlers(".*$", [handler])
        
        # Act
        response = self.fetch("/nodes",
                            method="POST",
                            body=json.dumps(node), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        
        # Assert
        self.assertEqual(response.code, 201)
        res_id = unicode(response.headers.get('Location', "").split('/')[-1])
        result = self.sync_db[self.collection_name].find_one({'id': res_id}, fields={"_id": 0})
        # Unescape special chars
        result = json.loads(dumps_mongo(result).replace("\\\\$", "$"))
        result.pop("ts", None)
        result.pop("id", None)
        result.pop("selfRef", None)
        self.maxDiff = None
        self.assertEqual(result, node)
        
    
    def test_post_get(self):
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['node']
        nodes_handler = ("/nodes$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['node']}))
        node_handler = ("/nodes/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['node']}))
        self._app.add_handlers(".*$", [nodes_handler, node_handler])
        node = self._create_node("node_test")
        # Act
        post_response = self.fetch("/nodes",
                            method="POST",
                            body=json.dumps(node), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        
        node_id = unicode(post_response.headers['Location'].split('/')[-1])
        node['id'] = node_id
        
        get_response = self.fetch("/nodes/%s" % node_id,
                            method="GET",
                            headers={"Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        ret_node = json.loads(get_response.body)
        ret_node.pop("ts")
        ret_node.pop("selfRef")
        self.assertEqual(node, ret_node)
    
    def test_put(self):
        # Arrange
        self.sync_db[self.collection_name].create_index([("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        good_request = {
            u"id": u"1",
            u"ts": 1330921125000000 ,
            u"name": u"host1"
        }
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/tests/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/tests",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        
        # Act
        good_response = self.fetch("/tests/1",
                            method="PUT",
                            body=json.dumps(good_request), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        
        # Assert
        self.assertEqual(good_response.code, 201)
        
    def test_delete(self):
        """Test retrieving each node"""
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        nodes = self._insert_nodes(5)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=False)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/nodes/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer,
                        base_url="/nodes",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])

        # Act
        responses = []
        for node in nodes:
            response = self.fetch("/nodes/" + node['id'], method="DELETE",
                    headers={"Accept": MIME['PSJSON'], "Connection": "keep-alive"})
            responses.append(response)
        
        responses_get = []
        for node in nodes:
            response = self.fetch("/nodes/" + node['id'],
                    headers={"Accept": MIME['PSJSON'], "Connection": "keep-alive"})
            responses_get.append(response)

        # Assert
        self.assertEqual(len(responses), len(nodes))
        for i in range(len(nodes)):
            response = responses[i]
            self.assertEqual(response.code, 200)
        
        self.assertEqual(len(responses_get), len(nodes))
        for i in range(len(nodes)):
            response = responses_get[i]
            self.assertEqual(response.code, 410)
            



class NetworkResourceHandlerTest(PeriscopeHTTPTestCase):
    def __init__(self, *args, **kwargs):
        super(NetworkResourceHandlerTest, self).__init__(*args, **kwargs)
    
    def get_app(self):
        return tornado.web.Application([])
    
    def setUp(self):
        super(NetworkResourceHandlerTest, self).setUp()

    def tearDown(self):
        super(NetworkResourceHandlerTest, self).tearDown()
    
    def test_accept_content_type(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"tests": None})
        dblayer_mock = Mock(spec=DBLayer)
        
        wildcard_request = Mock()
        wildcard_request.headers.get.return_value = "*/*"
        wildcard_handler = NetworkResourceHandler(app,
                            wildcard_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            accepted_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        psjson_request = Mock()
        psjson_request.headers.get.return_value = MIME['PSJSON']
        psjson_handler = NetworkResourceHandler(app,
                            psjson_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            accepted_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        psxml_request = Mock()
        psxml_request.headers.get.return_value = MIME['PSXML']
        psxml_handler = NetworkResourceHandler(app,
                            psxml_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            accepted_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        html_request = Mock()
        html_request.headers.get.return_value = MIME['HTML']
        html_handler = NetworkResourceHandler(app,
                            html_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            accepted_mime=[MIME['HTML']])
        
        multi_request = Mock()
        multi_request.headers.get.return_value = "%s,%s,%s" % (MIME['HTML'], MIME['PSJSON'], MIME['PSXML'])
        multi_handler = NetworkResourceHandler(app,
                            multi_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            accepted_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        text_request = Mock()
        text_request.headers.get.return_value = MIME['PLAIN']
        text_handler = NetworkResourceHandler(app,
                            text_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            accepted_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        # Act
        wildcard_ret = wildcard_handler.accept_content_type
        psjson_ret = psjson_handler.accept_content_type
        psxml_ret = psxml_handler.accept_content_type
        html_ret = html_handler.accept_content_type
        multi_ret = multi_handler.accept_content_type
        
        # Assert
        self.assertEqual(wildcard_ret, MIME['JSON'])
        self.assertEqual(psjson_ret, MIME['PSJSON'])
        self.assertEqual(psxml_ret, MIME['PSXML'])
        self.assertEqual(html_ret, MIME['HTML'])
        self.assertEqual(multi_ret, MIME['PSXML'])
        self.assertRaises(HTTPError, lambda : text_handler.accept_content_type)
    
    def test_content_type(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"tests": None})
        dblayer_mock = Mock(spec=DBLayer)
        
        psjson_request = Mock()
        psjson_request.headers.get.return_value = MIME['PSJSON'] + \
                    "; profile=http://unis.incntre.iu.edu/schema/20120709/networkresoruce"
        psjson_handler = NetworkResourceHandler(app,
                            psjson_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            content_types_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        psxml_request = Mock()
        psxml_request.headers.get.return_value = MIME['PSXML']
        psxml_handler = NetworkResourceHandler(app,
                            psxml_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            content_types_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        text_request = Mock()
        text_request.headers.get.return_value = MIME['PLAIN']
        text_handler = NetworkResourceHandler(app,
                            text_request,
                            dblayer=dblayer_mock,
                            base_url="/tests",
                            content_types_mime=[MIME['PSJSON'], MIME['PSXML']])
        
        # Act
        psjson_ret = psjson_handler.content_type
        psxml_ret = psxml_handler.content_type
        
        # Assert        
        self.assertEqual(psjson_ret, MIME['PSJSON'])
        self.assertEqual(psxml_ret, MIME['PSXML'])
        self.assertRaises(HTTPError, lambda : text_handler.content_type)
    
    def test_supports_streaming(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"tests": None})
        dblayer_mock = Mock(spec=DBLayer)
        
        psjson_request = Mock()
        psjson_request.headers.get.side_effect = \
            lambda k, d: {"Connection": "keep-alive", "Accept": MIME["PSJSON"]}[k]
        psjson_handler = NetworkResourceHandler(app,
                            psjson_request,
                            dblayer=dblayer_mock,
                            base_url="/tests")
        
        sse_request = Mock()
        sse_request.headers.get.side_effect = \
            lambda k, d: {"Connection": "keep-alive", "Accept": MIME["SSE"]}[k]
        sse_handler = NetworkResourceHandler(app,
                            sse_request,
                            dblayer=dblayer_mock,
                            base_url="/tests")
        
        html_request = Mock()
        html_request.headers.get.side_effect = \
            lambda k, d: {"Connection": "keep-alive", "Accept": MIME["HTML"]}[k]
        html_handler = NetworkResourceHandler(app,
                            html_request,
                            dblayer=dblayer_mock,
                            base_url="/tests")
        
        # Act
        psjson_ret = psjson_handler.supports_streaming
        sse_ret = sse_handler.supports_streaming
        html_ret = html_handler.supports_streaming
        
        # Aassert
        self.assertEqual(psjson_ret, True)
        self.assertEqual(sse_ret, True)
        self.assertEqual(html_ret, False)
    
    def test_dblayer(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"tests": None})
        dblayer_mock = Mock(spec=DBLayer)
        request = Mock()
        
        handler = NetworkResourceHandler(app,
                            request,
                            dblayer=dblayer_mock,
                            base_url="/tests")
        # Act
        dblayer = handler.dblayer
        
        # Assert
        self.assertEqual(dblayer, dblayer_mock)
    
    def test_put_psjson(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"test": None})
        bad_dblayer_mock = Mock(spec=DBLayer)
        good_dblayer_mock = Mock(spec=DBLayer)
        id_dblayer_mock = Mock(spec=DBLayer)
        valid_body = {"id": "1", "ts": 1330921125000000}
        psjson_header = "%s; profile=%s" % (MIME['PSJSON'], schemas['networkresource'])
                    
        # Bad request
        bad_request = Mock(body=valid_body)
        bad_request.headers.get.return_value = psjson_header
        bad_handler = NetworkResourceHandler(app,
                            bad_request,
                            dblayer=bad_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        # Good request
        good_request = Mock(body=json.dumps(valid_body))
        good_request.headers.get.return_value = psjson_header
        good_handler = NetworkResourceHandler(app,
                            good_request,
                            dblayer=good_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Different IDs
        id_request = Mock(body=json.dumps(valid_body))
        id_request.headers.get.return_value = psjson_header
        id_handler = NetworkResourceHandler(app,
                            id_request,
                            dblayer=id_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Act
        bad_handler.put_psjson("1")
        good_handler.put_psjson("1")
        id_handler.put_psjson("2")
        
        # Assert
        self.assertEqual(bad_handler._status_code, 400)
        self.assertEqual(bad_dblayer_mock.insert.called, False)
        self.assertNotEqual(good_handler._status_code, 400)
        #good_dblayer_mock.insert.assert_called_once_with(valid_body, callback=good_handler.on_put)
        self.assertEqual(id_handler._status_code, 400)
        self.assertEqual(id_dblayer_mock.insert.called, False)
    
    def test_put_bad_request(self):
        # Arrange
        dblayer_mock = Mock(spec=DBLayer)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/tests/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        request = {"randomvalue": 1}
        # Act
        response = self.fetch("/tests/1",
                            method="PUT",
                            body=json.dumps(request), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 400)
        self.assertIn(MIME['PSJSON'], response.headers.get("Content-Type"))
    
    def test_put_bad_url(self):
        # Arrange
        dblayer_mock = Mock(spec=DBLayer)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/tests$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        request = {"id": "1"}
        # Act
        response = self.fetch("/tests",
                            method="PUT",
                            body=json.dumps(request), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 400)
        self.assertIn(MIME['PSJSON'], response.headers.get("Content-Type"))
    
    def test_put_bad_schema(self):
        # Arrange
        dblayer_mock = Mock(spec=DBLayer)
        handler = ("/tests/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        request = {"id": "1"}
        # Act
        response = self.fetch("/tests/1",
                            method="PUT",
                            body=json.dumps(request), 
                            headers={
                                "Content-Type": MIME['PSJSON'] + '; profile=http://example.com/schema',
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 400)
        self.assertIn(MIME['PSJSON'], response.headers.get("Content-Type"))

    @patch.object(NetworkResourceHandler, 'on_put', mocksignature=True)
    def test_put_good_request(self, on_put_mock):
        # Arrange
        request = {"id": "1", "ts": 1330921125000000, "name": 'host1'}
        excpeted = copy.deepcopy(request)
        excpeted[u"\\$schema"] = schemas['networkresource']
        dblayer_mock = Mock(spec=DBLayer)
        dblayer_mock.insert.side_effect = \
            lambda *args, **kwargs: kwargs['callback'](request, error=None)
        
        on_put_mock.side_effect = lambda self, *args, **kwargs: self.finish()
        handler = ("/tests/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        
        # Act
        response = self.fetch("/tests/1",
                            method="PUT",
                            body=json.dumps(request), 
                            headers={
                                "Content-Type": MIME['PSJSON'] + '; profile=' + schemas['networkresource'],
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 200, msg=response.body)
        self.assertEqual(dblayer_mock.insert.call_count, 1)
        self.assertEqual(len(dblayer_mock.insert.call_args), 2)
        self.assertEqual(dblayer_mock.insert.call_args[0][0], excpeted)
        self.assertTrue(on_put_mock.called)
        self.assertEqual(len(on_put_mock.call_args), 2)
        self.assertEqual(on_put_mock.call_args[0][1], request)
        self.assertEqual(on_put_mock.call_args[0][2], None)
        
    def test_on_put(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"test": None})
        dblayer_mock = Mock(spec=DBLayer)
        psjson_header = "%s; profile=%s" % (MIME['PSJSON'], schemas['networkresource'])
        
        # Bad request
        bad_result = {u'connectionId': 1, u'ok': 0.0, u'err': "Some error", u'n': 0}
        bad_request = Mock()
        bad_request.headers.get.return_value = psjson_header
        bad_handler = NetworkResourceHandler(app,
                            bad_request,
                            dblayer=dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        # Good request
        ok_result = {u'connectionId': 1, u'ok': 1.0, u'err': None, u'n': 0}
        good_request = Mock()
        good_request.headers.get.return_value = psjson_header
        good_handler = NetworkResourceHandler(app,
                            good_request,
                            dblayer=dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Act
        bad_handler.on_put(bad_result, error="Some error")
        good_handler.on_put(ok_result, error=None, return_resource=False)
        
        # Assert
        self.assertEqual(bad_handler._status_code, 500)
        self.assertEqual(good_handler._status_code, 201)
    
    def test_post_psjson(self):
        # Arrange
        app = Mock(ui_methods={}, ui_modules={}, async_db={"test": None})
        
        bad_dblayer_mock = Mock(spec=DBLayer)
        with_id_dblayer_mock = Mock(spec=DBLayer)
        no_id_dblayer_mock = Mock(spec=DBLayer)
        array_with_id_dblayer_mock = Mock(spec=DBLayer)
        array_no_id_dblayer_mock = Mock(spec=DBLayer)
        
        valid_body_with_id = {"id": "1", "ts": 1330921125000000}
        valid_body_no_id = {"ts": 1330921125000000}
        valid_array_with_id = [
            {"id": "1", "ts": 1330921125000000},
            {"id": "2", "ts": 1330921125000000}
        ]
        valid_array_no_id = [
            {"ts": 1330921125000000},
            {"ts": 1330921125000000}
        ]
        psjson_header = "%s; profile=%s" % (MIME['PSJSON'], schemas['networkresource'])
                    
        # Bad request
        bad_request = Mock(body=json.dumps({"id": 1}))
        bad_request.headers.get.return_value = psjson_header
        bad_request.full_url.return_value = "http://localhost/resources"
        bad_handler = NetworkResourceHandler(app,
                            bad_request,
                            dblayer=bad_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Good with ID request
        with_id_request = Mock(name="aa", body=json.dumps(valid_body_with_id))
        with_id_request.headers.get.return_value = psjson_header
        with_id_request.full_url.return_value = "http://localhost/resources"
        with_id_handler = NetworkResourceHandler(app,
                            with_id_request,
                            dblayer=with_id_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Good with NO ID request
        no_id_request = Mock(body=json.dumps(valid_body_no_id))
        no_id_request.headers.get.return_value = psjson_header
        no_id_request.full_url.return_value = "http://localhost/resources"
        no_id_handler = NetworkResourceHandler(app,
                            no_id_request,
                            dblayer=no_id_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Good Array with IDs request
        array_with_id_request = Mock(body=json.dumps(valid_array_with_id))
        array_with_id_request.headers.get.return_value = psjson_header
        array_with_id_request.full_url.return_value = "http://localhost/resources"
        array_with_id_handler = NetworkResourceHandler(app,
                            array_with_id_request,
                            dblayer=array_with_id_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
        
        # Good Array with NO IDs request
        array_no_id_request = Mock(body=json.dumps(valid_array_no_id))
        array_no_id_request.headers.get.return_value = psjson_header
        array_no_id_request.full_url.return_value = "http://localhost/resources"
        array_no_id_handler = NetworkResourceHandler(app,
                            array_no_id_request,
                            dblayer=array_no_id_dblayer_mock,
                            model_class=Node,
                            base_url="/tests",
                            schemas_single={MIME['PSJSON']: schemas['networkresource']})
    
        # Act
        bad_handler.post_psjson()
        with_id_handler.post_psjson()
        no_id_handler.post_psjson()
        array_with_id_handler.post_psjson()
        array_no_id_handler.post_psjson()
        
        # Assert
        self.assertEqual(bad_handler._status_code, 400)
        self.assertEqual(bad_dblayer_mock.insert.called, False)
        
        self.assertNotEqual(with_id_handler._status_code, 400)
        #with_id_dblayer_mock.insert.assert_called_once_with(valid_body_with_id, callback=with_id_handler.on_post)
        
        self.assertNotEqual(no_id_handler._status_code, 400)
        no_id_inserted = no_id_dblayer_mock.insert.call_args[0][0][0]
        no_id_gen = no_id_inserted.pop("id", None)
        self.assertFalse(not no_id_gen)
        #no_id_dblayer_mock.insert.assert_called_once_with(valid_body_no_id, callback=no_id_handler.on_post)
        
        self.assertNotEqual(array_with_id_handler._status_code, 400)
    
    def test_post_bad_url(self):
        # Arrange
        dblayer_mock = Mock(spec=DBLayer)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        handler = ("/tests/(?P<res_id>[^\/]*)$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        request = {"id": "1"}
        # Act
        response = self.fetch("/tests/1",
                            method="POST",
                            body=json.dumps(request), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 400)
        self.assertIn(MIME['PSJSON'], response.headers.get("Content-Type"))
    
    def test_post_bad_schema(self):
        # Arrange
        dblayer_mock = Mock(spec=DBLayer)
        handler = ("/tests$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        request = {"id": "1"}
        content_type = MIME['PSJSON'] + ' ; profile=http://unis.incntre.iu.edu/schema/20120709/domain#'
        # Act
        response = self.fetch("/tests",
                            method="POST",
                            body=json.dumps(request), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 400)
        self.assertIn(MIME['PSJSON'], response.headers.get("Content-Type"))
    
    @patch.object(NetworkResourceHandler, 'on_post', mocksignature=True)
    def test_post_good_request(self, on_post_mock):
        # Arrange
        request_single = {
            u"id": u"1",
            u"ts": 1330921125000000 ,
            u"name": u"host1"
        }
        excpeted = copy.deepcopy(request_single)
        excpeted[u"\\$schema"] = schemas['networkresource']
        dblayer_mock = Mock(spec=DBLayer)
        dblayer_mock.insert.side_effect = \
            lambda *args, **kwargs: kwargs['callback'](request_single, error=None)
        
        on_post_mock.side_effect = lambda self, *args, **kwargs: self.finish()
        handler = ("/tests$", NetworkResourceHandler,
                   dict(dblayer=dblayer_mock,
                        base_url="/tests",
                        model_class=Node,
                        schemas_single={MIME['PSJSON']: schemas['networkresource']}))
        self._app.add_handlers(".*$", [handler])
        content_type = MIME['PSJSON'] + '; profile=' + schemas['networkresource']
        # Act
        response = self.fetch("/tests",
                            method="POST",
                            body=json.dumps(request_single), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 200, msg=response.body)
        self.assertEqual(dblayer_mock.insert.call_count, 1)
        self.assertEqual(len(dblayer_mock.insert.call_args), 2)
        excpeted["selfRef"] = dblayer_mock.insert.call_args[0][0][0].get("selfRef")
        self.assertEqual(dblayer_mock.insert.call_args[0][0], [excpeted])
        self.assertTrue(on_post_mock.called)
        self.assertEqual(len(on_post_mock.call_args), 2)
        self.assertEqual(on_post_mock.call_args[0][1], request_single)
        self.assertEqual(on_post_mock.call_args[0][2], None)




class CollectionHandlerIntegrationTest(PeriscopeHTTPTestCase):
    def __init__(self, *args, **kwargs):
        super(CollectionHandlerIntegrationTest, self).__init__(*args, **kwargs)
        self.collection_name = "test_collection"

    def setUp(self):
        super(CollectionHandlerIntegrationTest, self).setUp()
        self.default_resource_settings = {
            "base_url": "", 
            "handler_class": "periscope.handlers.NetworkResourceHandler",
            "is_capped_collection": False,
            "capped_collection_size": 0,
            "id_field_name": "id",
            "timestamp_field_name": "ts",
            "allow_get": True,
            "allow_post": True,
            "allow_put": True,
            "allow_delete": False,
            "accepted_mime": [MIME['SSE'], MIME['PSJSON']],
            "content_types_mime": [MIME['SSE'], MIME['PSJSON']]
        }
        self.node_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "node",
                    "pattern": "/nodes/(?P<res_id>[^\/]*)$",
                    "model_class": "periscope.models.Node",
                    "collection_name": "nodes",
                    "schema": {MIME['PSJSON']: schemas["node"]},
                }.items()
            )
        self.nodes_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "nodes",
                    "pattern": "/nodes",
                    "model_class": "periscope.models.Node",
                    "collection_name": "nodes",
                    "schema": {MIME['PSJSON']: schemas["node"]},
                }.items()
            )
        self.port_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "port",
                    "pattern": "/ports/(?P<res_id>[^\/]*)$",
                    "model_class": "periscope.models.Port",
                    "collection_name": "ports",
                    "schema": {MIME['PSJSON']: schemas["port"]},
                }.items()
            )
        self.ports_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "ports",
                    "pattern": "/ports",
                    "model_class": "periscope.models.Port",
                    "collection_name": "ports",
                    "schema": {MIME['PSJSON']: schemas["port"]},
                }.items()
            )
        self.link_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "link",
                    "pattern": "/links/(?P<res_id>[^\/]*)$",
                    "model_class": "periscope.models.Link",
                    "collection_name": "links",
                    "schema": {MIME['PSJSON']: schemas["link"]},
                }.items()
            )
        self.links_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "links",
                    "pattern": "/links",
                    "model_class": "periscope.models.Link",
                    "collection_name": "links",
                    "schema": {MIME['PSJSON']: schemas["link"]},
                }.items()
            )
        self.service_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "service",
                    "pattern": "/services/(?P<res_id>[^\/]*)$",
                    "model_class": "periscope.models.Service",
                    "collection_name": "services",
                    "schema": {MIME['PSJSON']: schemas["service"]},
                }.items()
            )
        self.services_settings = dict(self.default_resource_settings.items() + \
                {
                    "name": "services",
                    "pattern": "/services",
                    "model_class": "periscope.models.Service",
                    "collection_name": "services",
                    "schema": {MIME['PSJSON']: schemas["service"]},
                }.items()
            )
        self.topology_settings = dict(self.default_resource_settings.items() + \
            {
                "name": "topology",
                "pattern": "/topologies/(?P<res_id>[^\/]*)$",
                "model_class": "periscope.models.Topology",
                "collection_name": "topologies",
                "schema": {MIME['PSJSON']: schemas["topology"]},
            }.items()
        )
        self.domain_settings = dict(self.default_resource_settings.items() + \
            {
                "name": "domain",
                "pattern": "/domains/(?P<res_id>[^\/]*)$",
                "model_class": "periscope.models.Domain",
                "collection_name": "domains",
                "schema": {MIME['PSJSON']: schemas["domain"]},
            }.items()
        )
        self.resources_settings = {
            "links": self.links_settings,
            "ports": self.ports_settings,
            "nodes": self.nodes_settings,
            "services": self.services_settings,
        }
        self.collections_settings = {
            "links": self.link_settings,
            "ports": self.port_settings,
            "nodes": self.node_settings,
            "services": self.service_settings,
            "topologies": self.topology_settings,
            "domains": self.domain_settings,
        }
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)
        self.sync_db.create_collection(self.collection_name,
            capped=True, size=100)
        for value in self.collections_settings.values():
            self.sync_db.drop_collection(value["collection_name"])
            self.sync_db.create_collection(value["collection_name"],
                capped=True, size=100)
    
    def tearDown(self):
        super(CollectionHandlerIntegrationTest, self).tearDown()
        # make sure we start by clean collection for each test case
        self.sync_db.drop_collection(self.collection_name)
        for value in self.collections_settings.values():
            self.sync_db.drop_collection(value["collection_name"])
            
    def _get_sample_topology(self):
        """Returns sample topology for testing"""
        topology = {
            u"$schema": u"http://unis.incntre.iu.edu/schema/20120709/topology#",
            u"nodes": [
                {
                    u"$schema": u"http://unis.incntre.iu.edu/schema/20120709/node#",
                    u"description": u"LAMP node",
                    u"ports": [
                        {
                            u"href": u"#/ports/0/",
                            u"rel": u"full"
                        }
                    ],
                    u"properties": {
                        u"prop1": 1,
                        u"prop2": 1,
                        u"prop3": 3
                    }
                },
                {
                    u"$schema": u"http://unis.incntre.iu.edu/schema/20120709/node#",
                    u"description": u"LAMP node",
                    u"ports": [
                        {
                            u"href": u"#/ports/1",
                            u"rel": u"full"
                        }
                    ],
                    u"properties": {
                        u"prop1": 1,
                        u"prop2": 1,
                        u"prop3": 3
                    }
                }
            ],
            u"ports": [
                {
                    u"$schema": u"http://unis.incntre.iu.edu/schema/20120709/port#",
                    u"address": {u"address": u"10.10.1.1", u"type": u"ipv4"},
                    u"name": u"eth1",
                },
                {
                    u"$schema": u"http://unis.incntre.iu.edu/schema/20120709/port#",
                    u"address": {u"address": u"10.10.1.3", u"type": u"ipv4"},
                    u"name": u"eth3",
                }
            ]
        }
        return topology
    
    def test_post(self):
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        topology = self._get_sample_topology()
        content_type = MIME['PSJSON'] + '; profile=' + schemas['topology']
        handler = ("/topologies$", CollectionHandler,
                   dict(collections=self.collections_settings,
                        dblayer=dblayer,
                        base_url="/topologies",
                        model_class=Topology,
                        schemas_single={MIME['PSJSON']: schemas['topology']}))
        handlers = [handler]
        handlers += self._make_handlers()
        self._app.add_handlers(".*$", handlers)
        # Act
        response = self.fetch("/topologies",
                            method="POST",
                            body=json.dumps(topology), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 201, msg=response.body)
        res_id = unicode(response.headers.get('Location', "").split('/')[-1])
        topology_rep = self.sync_db[self.collection_name].find_one({'id': res_id})        
        self.assertTrue(isinstance(topology_rep, dict))
        settings = self.collections_settings
        nodes = list(self.sync_db[settings["nodes"]["collection_name"]].find())
        ports = list(self.sync_db[settings["ports"]["collection_name"]].find())
        links = list(self.sync_db[settings["links"]["collection_name"]].find())
        
        self.assertEqual(len(nodes), 2)
        self.assertEqual(len(ports), 2)
        self.assertEqual(len(links), 0)
        
        expected = copy.deepcopy(topology)
        expected["nodes"][0]["ports"][0]["href"] = ports[0]["selfRef"]
        expected["nodes"][1]["ports"][0]["href"] = ports[1]["selfRef"]
        self.assertTrue("/topologies/" in topology_rep.get("selfRef", ""))
        
        for name, settings in self.collections_settings.items():
            mongo_name = settings["collection_name"]
            results = self.sync_db[mongo_name].find()
            counter = 0
            for result in results:
                self.assertIsNotNone(result.pop("id", None))
                self.assertIsNotNone(result.pop("ts", None))
                self.assertIsNotNone(result.pop("selfRef", None))
                result.pop("_id", None)
                result["$schema"] = result.pop("\\$schema")
                self.assertEqual(expected[name][counter], result)
                counter += 1
    
    def test_get(self):
        # Arrange
        topology = {
            "\$schema": "http://unis.incntre.iu.edu/schema/20120709/topology#",
            "id": "4fa32f84f473537ce5000005",
            "selfRef": "http://localhost:10001/4fa32f84f473537ce5000005",
            "ts": 1336094596464475,
            "ports": [
                {
                    "selfRef": "http://localhost:10001/ports/4fa32f84f473537ce5000003"
                }, 
                {
                    "selfRef": "http://localhost:10001/ports/4fa32f84f473537ce5000004"
                }
            ], 
            "nodes": [
                {
                    "selfRef": "http://localhost:10001/nodes/4fa32f84f473537ce5000001"
                }, 
                {
                    "selfRef": "http://localhost:10001/nodes/4fa32f84f473537ce5000002"
                }
            ],
        }
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        self.sync_db[self.collection_name].insert(copy.deepcopy(topology))
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['topology']
        handler = ("/topologies/(?P<res_id>[^\/]*)$", CollectionHandler,
                   dict(collections=self.collections_settings,
                        dblayer=dblayer,
                        base_url="/topologies",
                        model_class=Topology,
                        schemas_single={MIME['PSJSON']: schemas['topology']}))
        self._app.add_handlers(".*$", [handler])
        # Act
        response = self.fetch("/topologies/" + topology["id"],
                            method="GET",
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(response.code, 200)
        topology["$schema"] = topology.pop("\$schema")
        self.assertEqual(json.loads(response.body), topology)
    
    def _make_handlers(self):
        """Makes the differnet handlers from self.collections_settings."""
        handlers = []
        for settings in self.collections_settings.values():
            # Load classes
            handler_class = load_class(settings["handler_class"])
            db_layer = self._app.get_db_layer(settings["collection_name"],
                        settings["id_field_name"],
                        settings["timestamp_field_name"],
                        settings["is_capped_collection"],
                        settings["capped_collection_size"])
            # Make the handler
            handler = (
                tornado.web.URLSpec(settings["base_url"] + settings["pattern"],
                    handler_class,
                    dict(
                        dblayer=db_layer,
                        Id=settings["id_field_name"],
                        timestamp=settings["timestamp_field_name"],
                        base_url=settings["base_url"]+settings["pattern"],
                        allow_delete=settings["allow_delete"],
                        schemas_single=settings["schema"],
                        model_class=settings["model_class"]
                    ),
                    name=settings["name"]
                )
            )
            handlers.append(handler)
        
        for settings in self.resources_settings.values():
            # Load classes
            handler_class = load_class(settings["handler_class"])
            db_layer = self._app.get_db_layer(settings["collection_name"],
                        settings["id_field_name"],
                        settings["timestamp_field_name"],
                        settings["is_capped_collection"],
                        settings["capped_collection_size"])
            # Make the handler
            handler = (
                tornado.web.URLSpec(settings["base_url"] + settings["pattern"],
                    handler_class,
                    dict(
                        dblayer=db_layer,
                        Id=settings["id_field_name"],
                        timestamp=settings["timestamp_field_name"],
                        base_url=settings["base_url"]+settings["pattern"],
                        allow_delete=settings["allow_delete"],
                        schemas_single=settings["schema"],
                        model_class=load_class(settings["model_class"])
                    ),
                    name=settings["name"]
                )
            )
            handlers.append(handler)
        return handlers
        
    def test_post_get(self):
        # Arrange
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name, capped=True)
        topology = self._get_sample_topology()
        content_type = MIME['PSJSON'] + '; profile=' + schemas['topology']
        handler = ("/topologies$", CollectionHandler,
                   dict(collections=self.collections_settings,
                        dblayer=dblayer,
                        base_url="/topologies",
                        model_class=Topology,
                        schemas_single={MIME['PSJSON']: schemas['topology']}))
        handler_single = ("/topologies/(?P<res_id>[^\/]*)$", CollectionHandler,
                   dict(collections=self.collections_settings,
                        dblayer=dblayer,
                        base_url="/topologies",
                        model_class=Topology,
                        schemas_single={MIME['PSJSON']: schemas['topology']}))
        handlers = [handler_single, handler]
        handlers += self._make_handlers()
        self._app.add_handlers(".*$", handlers)
        # Act
        post_response = self.fetch("/topologies",
                            method="POST",
                            body=json.dumps(topology), 
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        res_id = unicode(post_response.headers.get('Location').split('/')[-1])
        get_response = self.fetch("/topologies/" + res_id,
                            method="GET",
                            headers={
                                "Content-Type": content_type,
                                "Cache-Control": "no-cache",
                                "Accept": MIME['PSJSON'],
                                "Connection": "close"})
        # Assert
        self.assertEqual(post_response.code, 201)
        self.assertEqual(get_response.code, 200)
        get_body = json.loads(get_response.body)
        self.assertTrue("nodes" in get_body)
        self.assertTrue("ports" in get_body)
        nodes = get_body["nodes"]
        ports = get_body["ports"]
        self.assertEqual(len(nodes), 2)
        self.assertEqual(len(ports), 2)
    
    def test_complete_href_links_jsonpoitner(self):
        # Arrange
        topology = {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/topology#",
            "id": "4fa32f84f473537ce5000005",
            "ts": 1336094596464475,
            "ports": [
                {
                    "selfRef": "http://example.com/ports/1"
                }, 
                {
                    "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                    "urn": "urn:ogf:network:domain=example.com:port=2",
                    "name": "port2",
                }
            ], 
            "nodes": [
                {
                    "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
                    "id": 1,
                    "name": "node1",
                    "ports": [
                        {
                            "href": "#/ports/0",
                            "rel": "full"
                        },
                        {
                            "href": "#/ports/1",
                            "rel": "full"
                        }
                    ]
                }, 
                {
                    "selfRef": "http://example.com/nodes/2"
                }
            ],
        }
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name,
            capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['topology']
        request = HTTPRequest("GET", "http://example.com/topologies/1",
                version="HTTP/1.1", connection=Mock())
        self._app.add_handlers(".*$", self._make_handlers())
        handler = CollectionHandler(self._app, request,
                collections=self.collections_settings,
                dblayer=dblayer,
                base_url="/topologies",
                model_class=Topology,
                schemas_single={MIME['PSJSON']: schemas['topology']})

        # Act
        topology_obj = Topology(topology, schemas_loader=schemaLoader)
        handler._complete_href_links(topology_obj, topology_obj)
        
        # Assert
        port1_href = topology_obj["nodes"][0]["ports"][0]["href"]
        self.assertEqual(port1_href, "http://example.com/ports/1")
        port2_href = topology_obj["nodes"][0]["ports"][1]["href"]
        self.assertTrue(port2_href.startswith("http://"))
        self.assertTrue(port2_href.endswith("/ports/" + topology_obj["ports"][1]["id"]))
        
    
    def test_complete_href_links_jsonpath(self):
        # Arrange
        topology = {
            "$schema": "http://unis.incntre.iu.edu/schema/20120709/topology#",
            "id": "4fa32f84f473537ce5000005",
            "ts": 1336094596464475,
            "ports": [
                {
                    "selfRef": "http://example.com/ports/1"
                }, 
                {
                    "$schema": "http://unis.incntre.iu.edu/schema/20120709/port#",
                    "urn": "urn:ogf:network:domain=example.com:port=2",
                    "name": "port2",
                }
            ], 
            "nodes": [
                {
                    "$schema": "http://unis.incntre.iu.edu/schema/20120709/node#",
                    "id": 1,
                    "name": "node1",
                    "ports": [
                        {
                            "href": "$.ports[0]",
                            "rel": "full"
                        },
                        {
                            "href": "$..[?(@.name=='port2')]",
                            "rel": "full"
                        }
                    ]
                }, 
                {
                    "selfRef": "http://example.com/nodes/2"
                }
            ],
        }
        self.sync_db[self.collection_name].create_index(
                            [("id", 1), ("ts", 1)], unique=True)
        dblayer = DBLayer(self.async_db, self.collection_name,
            capped=True)
        content_type = MIME['PSJSON'] + '; profile=' + schemas['topology']
        request = HTTPRequest("GET", "http://example.com/topologies/1",
                version="HTTP/1.1", connection=Mock())
        self._app.add_handlers(".*$", self._make_handlers())
        handler = CollectionHandler(self._app, request,
                collections=self.collections_settings,
                dblayer=dblayer,
                base_url="/topologies",
                model_class=Topology,
                schemas_single={MIME['PSJSON']: schemas['topology']})

        # Act
        topology_obj = Topology(topology, schemas_loader=schemaLoader)
        handler._complete_href_links(topology_obj, topology_obj)
        
        # Assert
        port1_href = topology_obj["nodes"][0]["ports"][0]["href"]
        self.assertEqual(port1_href, "http://example.com/ports/1")
        port2_href = topology_obj["nodes"][0]["ports"][1]["href"]
        self.assertTrue(port2_href.startswith("http://"))
        self.assertTrue(port2_href.endswith("/ports/" + topology_obj["ports"][1]["id"]))

