#!/usr/bin/env python
"""
Periscope HTTP(s) Handlers.
"""

import copy
import json
import re
import functools
import jsonpointer
from jsonpath import jsonpath
from netlogger import nllog
import time
import urllib2
import traceback
from tornado.ioloop import IOLoop
import tornado.gen as gen
import tornado.web
from tornado.httpclient import HTTPError
from tornado.httpclient import AsyncHTTPClient
import pymongo
if pymongo.version_tuple[1] > 1:
    from bson.objectid import ObjectId
else:
    from pymongo.objectid import ObjectId

from urllib import urlencode

from periscope.db import DBLayer
from periscope.db import dumps_mongo
from periscope.models import ObjectDict
from periscope.models import NetworkResource
from periscope.models import HyperLink
from periscope.models import Topology
from periscope.models import schemaLoader
from periscope.models import JSONSchemaModel
import periscope.utils as utils
from asyncmongo.errors import IntegrityError

MIME = {
    'HTML': 'text/html',
    'JSON': 'application/json',
    'PLAIN': 'text/plain',
    'SSE': 'text/event-stream',
    'PSJSON': 'application/perfsonar+json',
    'PSXML': 'application/perfsonar+xml',
}

SCHEMAS = {
    'networkresource': 'http://unis.incntre.iu.edu/schema/20120709/networkresource#',
    'node': 'http://unis.incntre.iu.edu/schema/20120709/node#',
    'domain': 'http://unis.incntre.iu.edu/schema/20120709/domain#',
    'port': 'http://unis.incntre.iu.edu/schema/20120709/port#',
    'link': 'http://unis.incntre.iu.edu/schema/20120709/link#',
    'path': 'http://unis.incntre.iu.edu/schema/20120709/path#',
    'network': 'http://unis.incntre.iu.edu/schema/20120709/network#',
    'topology': 'http://unis.incntre.iu.edu/schema/20120709/topology#',
    'blipp': 'http://unis.incntre.iu.edu/schema/20120709/blipp#',
    'metadata': 'http://unis.incntre.iu.edu/schema/20120709/metadata#',
    'service' : "http://unis.incntre.iu.edu/schema/20120709/service#"
}

# TODO (AH): cache common schemas locally
# TODO (AH): This is a very ugly way of handling cache!
CACHE = {
    "http://json-schema.org/draft-03/links#": {
        "additionalProperties": True,
        "type": "object"
    },
    "http://json-schema.org/draft-03/hyper-schema#": {
        "additionalProperties": True,
        "type": "object"
    },
}


class SSEHandler(tornado.web.RequestHandler):
    """
    Handles Server-Sent Events (SSE) requests as specified in
    http://dev.w3.org/html5/eventsource/.

    This handlers gives the option to to the user to use SSE or any other
    regular MIME types in the same same handler. If the MINE type of the
    request is 'text/event-stream' by default this handler is going to
    respond by 'text/event-stream' Content-Type.

    Examlpe::

        class MyHandler(SSEHandler):
            def periodic_send_events(self):
                # First check if the client didn't go away
                if self.request.connection.stream.closed():
                    self._periodic_sse.stop()
                    return
                # just print the current server's timestamp to the user
                t = time.time()
                self.write_event("id_%d" % int(t), "message",
                    "time is %d; last event id was %s" %
                    (t, self.get_last_event_id()))

            @tornado.web.asynchronous
            def get(self):
                if self.supports_sse():
                    self._periodic_sse = tornado.ioloop.PeriodicCallback(
                                            self.periodic_send_events, 2000)
                    self._periodic_sse.start( )
                else:
                    self.write("This was not server sent event request")
                    self.finish()

            def post(self):
                # just to show this is a regular request handler
                if self.supports_sse():
                    self.write_event('post','message', self.request.body)
    """

    SSE_MIME = "text/event-stream"
    # Default client connection retry time.
    DEFAULT_RETRY = 5000

    def get_last_event_id(self):
        """
        Returns the value of the last event id sent to the client or.
        For connection retry, returns Last-Event-ID header field.
        """
        return getattr(self, '_last_event_id', None)

    def supports_sse(self):
        """
        Returen True if 'text/event-stream' was in the HTTP's Accpet field.
        """
        return getattr(self, '_supports_sse', False)

    def write_event(self, event_id=None, event=None, data=None):
        """
        Writes a server sent event to the client. event_id is optional
        unique ID for the event. event is optional event's name.

        At the fist look it might look weird to have all function parameters
        set to None by default. However, the SSE specification does not
        specifiy any required fields so it's completely legal to send nothing!
        """
        # Escape values
        if event_id:
            event_id = tornado.escape.utf8(event_id)
        if event:
            event = tornado.escape.utf8(event)
        if data:
            data = tornado.escape.utf8(data).strip()
        else:
            raise TypeError("data must be defined.")
        # Check data types
        if event_id.find("\n") > -1 or event_id.find("\r") > -1:
            raise TypeError("Event ID cannot have new lines.")
        if event.find("\n") > -1 or event_id.find("\r") > -1:
            raise TypeError("Event cannot have new lines.")
        # Handles multiline data
        data = data.replace("\n", "\ndata:")
        # Construct a message to be sent
        message = ""
        if event_id:
            message += "id:%s\n" % event_id
            self._last_event_id = event_id
        if event:
            message += "event:%s\n" % event
        if data:
            message += "data:%s\n\n" % data
        # write and flush the event to the stream
        self.write(message)
        self.flush()

    def set_retry(self, retry):
        """
        Set the connection retry time for the client in case if the connection
        failed unexpectedly.
        """
        self.write("retry:%d\n\n" % int(retry))
        self.flush()

    def write_heartbeat(self):
        """
        Writes a message that is igonored by the client. This is usefull
        for old proxies not to terminate the HTTP connection unexpectedly.
        See: http://dev.w3.org/html5/eventsource/#notes for more information.
        """
        if self.request.connection.stream.closed():
            return

        self.write(":\n\n")
        self.flush()

    def decide_content_type(self):
        """
        A hook for HTTP content negotiation .
        """
        if self.request.headers.get("Accept", "").find(self.SSE_MIME) > -1:
            return self.SSE_MIME
        else:
            return self.request.headers.get("Accept", None)

    def _execute(self, transforms, *args, **kwargs):
        """Executes this request with the given output transforms."""
        self._transforms = transforms
        try:
            if self.request.method not in self.SUPPORTED_METHODS:
                raise HTTPError(405)
            # If XSRF cookies are turned on, reject form submissions without
            # the proper cookie
            if self.request.method not in ("GET", "HEAD", "OPTIONS") and \
               self.application.settings.get("xsrf_cookies"):
                self.check_xsrf_cookie()
            # Handles Server Sent Events requests
            if self.decide_content_type() == self.SSE_MIME:
                self._supports_sse = True
                self._last_event_id = self.request.headers.get("Last-Event-ID",
                                            None)
                self.set_header("Cache-Control", "no-cache")
                self.set_header("Content-Type", self.SSE_MIME)
                if self.DEFAULT_RETRY:
                    self.set_retry(self.DEFAULT_RETRY)
            else:
                self._supports_sse = False
            self.prepare()
            if not self._finished:
                args = [self.decode_argument(arg) for arg in args]
                kwargs = dict((k, self.decode_argument(v, name=k))
                              for (k, v) in kwargs.iteritems())
                getattr(self, self.request.method.lower())(*args, **kwargs)
                if self._auto_finish and not self._finished:
                    self.finish()
        except Exception, e:
            self._handle_request_exception(e)


class NetworkResourceHandler(SSEHandler, nllog.DoesLogging):
    """Generic Network resources handler"""

    def initialize(self, dblayer, base_url,
            Id="id",
            timestamp="ts",
            schemas_single=None,
            schemas_list=None,
            allow_get=False,
            allow_post=True,
            allow_put=True,
            allow_delete=True,
            tailable=False,
            model_class=None,
            accepted_mime=[MIME['SSE'], MIME['PSJSON'], MIME['PSXML']],
            content_types_mime=[MIME['SSE'],
                        MIME['PSJSON'], MIME['PSXML'], MIME['HTML']]):
        """
        Initializes handler for certain type of network resources.

        Parameters:
        
        collection_name: name of the database collection name that
                        stores information about the network resource.
        
        base_url: the base the path to access this resource, e.g., /nodes
        
        schemas_single: a dictionary that represents the network
                        resources schema to be validated againest.
                        The dictionary is indexed by content-type.
        
        schemas_list: a dictionary that represents the listing of this
                        resources schema to be validated againest.
        
        allow_get: User client can issue HTTP GET requests to this resource
        
        allow_post: User client can issue HTTP POST requests to this resource
        
        allow_put: User client can issue HTTP PUT requests to this resource
        
        allow_delete: User client can issue HTTP DELETE requests to this
                        resource.
        
        tailable: The underlying database collection is a capped collection.
        """
        # TODO (AH): Add ability to Enable/Disable different HTTP methods
        #if not isinstance(dblayer, DBLayer):
        #    raise TypeError("dblayer is not instance of DBLayer")
        self.Id = Id
        self.timestamp = timestamp
        self._dblayer = dblayer
        self._base_url = base_url
        self.schemas_single = schemas_single
        self.schemas_list = schemas_list
        self._allow_get = allow_get
        self._allow_post = allow_post
        self._allow_put = allow_put
        self._allow_delete = allow_delete
        self._accepted_mime = accepted_mime
        self._content_types_mime = content_types_mime
        self._tailable = tailable
        self._model_class = model_class
        if self.schemas_single is not None and \
            MIME["JSON"] not in self.schemas_single and \
            MIME["PSJSON"] in self.schemas_single:
                self.schemas_single[MIME["JSON"]] = self.schemas_single[MIME["PSJSON"]]
        if tailable and allow_delete:
            raise ValueError("Capped collections do not support" + \
                            "delete operation")

    @property
    def dblayer(self):
        """Returns a reference to the DB Layer."""
        if not getattr(self, "_dblayer", None):
            raise TypeError("No DB layer is defined for this handler.")
        return self._dblayer

    @property
    def accept_content_type(self):
        """
        HTTP has methods to allow the client and the server to negotiate
        the content type for their communication.

        Rigth now, this is simple implementation, but additional more complex
        methods can be added in the future.

        See:
            http://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html
            
            http://www.ietf.org/rfc/rfc2295.txt
            
            http://httpd.apache.org/docs/2.2/content-negotiation.html
            
            http://www.w3.org/TR/webarch/#def-coneg
        """
        if not getattr(self, '_accept', None):
            self._accept = None
            raw = self.request.headers.get("Accept", MIME['PSJSON'])
            regex = re.findall(
                "(?P<type>(\w+|\*)\/(\w+|\*)(\+\w+)?)(;[^;,]*)?([ ]*,[ ]*)?",
                raw
            )
            accept = [k[0] for k in regex]
            for accepted_mime in self._accepted_mime:
                if accepted_mime in accept:
                    self._accept = accepted_mime
            if "*/*" in accept:
                self._accept = MIME['JSON']
            if not self._accept:
                raise HTTPError(406,
                    "Unsupported accept content type '%s'" %
                    self.request.headers.get("Accept", None))
        return self._accept

    @property
    def content_type(self):
        """
        Returns the content type of the client's request

        See:
            
            http://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html
            
            http://www.ietf.org/rfc/rfc2295.txt
            
            http://httpd.apache.org/docs/2.2/content-negotiation.html
            
            http://www.w3.org/TR/webarch/#def-coneg
        """
        if not getattr(self, '_content_type', None):
            raw = self.request.headers.get("Content-Type", MIME['PSJSON'])
            regex = re.findall(
                "(?P<type>\w+\/\w+(\+\w+)?)(;[^;,]*)?([ ]*,[ ]*)?",
                raw
            )
            content_type = [k[0] for k in regex]
            for accepted_mime in self._content_types_mime:
                if accepted_mime in content_type:
                    self._content_type = accepted_mime
                    return self._content_type
            raise HTTPError(415,
                "Unsupported content type '%s'" %
                    self.request.headers.get("Content-Type", ""))
        return self._content_type

    @property
    def supports_streaming(self):
        """
        Returns true if the client asked for HTTP Streaming support.

        Any request that is of type text/event-stream or application/json
        with Connection = keep-alive is considered a streaming request
        and it's up to the client to close the HTTP connection.
        """
        if self.request.headers.get("Connection", "").lower() == "keep-alive":
            return self.request.headers.get("Accept", "").lower() in \
                    [MIME['PSJSON'], MIME['SSE']]
        else:
            return False

    def write_error(self, status_code, **kwargs):
        """
        Overrides Tornado error writter to produce different message
        format based on the HTTP Accept header from the client.
        """
        if self.settings.get("debug") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            content_type = self.accept_content_type or MIME['PSJSON']
            self.set_header("Content-Type", content_type)
            result = "{"
            for key in kwargs:
                result += '"%s": "%s",' % (key, kwargs[key])
            result = result.rstrip(",") + "}\n"
            self.write(result)
            self.finish()

    def _parse_get_arguments(self):
        """Parses the HTTP GET areguments given by the user."""
        def convert_value_type(key, value, val_type):
            if val_type == "integer":
                try:
                    return int(value)
                except:
                    raise HTTPError(400,
                        message="'%s' is not of type '%s'" % (key, val_type))
            if val_type == "number":
                try:
                    return float(value)
                except:
                    raise HTTPError(400,
                        message="'%s' is not of type '%s'" % (key, val_type))
            if val_type == "string":
                try:
                    return unicode(value)
                except:
                    raise HTTPError(400,
                        message="'%s' is not of type '%s'" % (key, val_type))
            if val_type == "boolean":
                try:
                    bools = {"true": True, "false": False, "1": True, "0": False}
                    return bools[value.lower()]
                except:
                    raise HTTPError(400,
                        message="'%s' is not of type '%s'" % (key, val_type))
            raise HTTPError(400,
                        message="Unkown value type '%s' for '%s'." % (val_type, key))
            
        def process_value(key, value):
            val = None
            in_split = value.split(",")
            if len(in_split) > 1:
                return process_in_query(key, in_split)[key]
            operators = ["lt", "lte", "gt", "gte"]
            for op in operators:
                if value.startswith(op + "="):
                    val = {"$"+ op: process_value(key, value.lstrip(op + "="))}
                    return val
            value_types = ["integer", "number", "string", "boolean"]
            for t in value_types:
                if value.startswith(t + ":"):
                    val = convert_value_type(key, value.split(t + ":")[1], t)
                    return val
            
            if key in ["ts", "ttl"]:
                val = convert_value_type(key, value, "number")
                return val
            return value
                
        def process_in_query(key, values):
            in_q = [process_value(key, val) for val in values]       
            return {key: {"$in": in_q}}
        
        def process_or_query(key, values):
            or_q = []
            if key:
                or_q.append({key: process_value(key, values[0])})
                values = values[1:]
            for val in values:
                keys_split = val.split("=", 1)
                if len(keys_split) != 2:
                    raise HTTPError(400, message="Not valid OR query.")
                k = keys_split[0]
                v = keys_split[1]
                or_q.append({k: process_value(k, v)})
            return {"$or": or_q}
            
        def process_and_query(key, values):
            and_q = []
            for val in values:
                split_or = val.split("|")
                if len(split_or) > 1:
                    and_q.append(process_or_query(key, split_or))
                    continue
                split = val.split(",")
                if len(split) == 1:
                    and_q.append({key: process_value(key, split[0])})
                else:
                    and_q.append(process_in_query(key, split))
            return {"$and": and_q}
        
        query = copy.copy(self.request.arguments)
        # First Reterive special parameters
        # fields
        fields = self.get_argument("fields", {})
        query.pop("fields", None)
        if fields:
            fields = dict([(name, 1) for name in fields.split(",")])
        # max results
        limit = self.get_argument("limit", default=None)
        query.pop("limit", None)
        if limit:
            limit = convert_value_type("limit", limit, "integer")
        
        query_ret = []
        for arg in query:
            if isinstance(query[arg], list) and len(query[arg]) > 1:
                and_q = process_and_query(arg, query[arg])
                query_ret.append(and_q)
                continue
            query[arg] = ",".join(query[arg])
            
            split_or = query[arg].split("|")
            if len(split_or) > 1:
                query_ret.append(process_or_query(arg, split_or))
                continue
            split = query[arg].split(",")
            if len(split) > 1:
                in_q = process_in_query(arg, split)
                query_ret.append(in_q)
            else:
                query_ret.append({arg: process_value(arg, split[0])})
        if query_ret:
            query_ret = {"$and": query_ret}
        else:
            query_ret = {}
        ret_val = {"fields": fields, "limit": limit, "query": query_ret}
        return ret_val

    def _get_cursor(self):
        """Returns reference to the database cursor."""
        return self._cursor

    @tornado.web.asynchronous
    @tornado.web.removeslash
    def get(self, res_id=None):
        """Handles HTTP GET"""
        accept = self.accept_content_type
        if res_id:
            self._res_id = unicode(res_id)
        else:
            self._res_id = None
        parsed = self._parse_get_arguments()
        query = parsed["query"]
        fields = parsed["fields"]
        limit = parsed["limit"]
        is_list = not res_id
        if query:
            is_list = True
        if is_list:
            query["status"] = {"$ne": "DELETED"}
        callback = functools.partial(self._get_on_response,
                            new=True, is_list=is_list, query=query)
        self._find(query, callback, fields=fields, limit=limit)

    def _find(self, query, callback, fields=None, limit=None):
        """Query the database.

        Parameters:

        callback: a function to be called back in case of new data.
                callback function should have `response`, `error`,
                and `new` fields. `new` is going to be True.
        """
        keep_alive = self.supports_streaming or self.supports_sse()
        if self._res_id:
            query[self.Id] = self._res_id
        options = dict(query=query, callback=callback)#, await_data=True)
        # Makes it a tailable cursor
        if keep_alive and self._tailable:
            options.update(dict(tailable=True, timeout=False))
        if fields:
            options["fields"] = fields
        if limit:
            options["limit"] = limit
        if "sort" not in options:
            options["sort"] = []
        options["sort"].append(("ts", -1))
        self._query = query
        self._cursor = self.dblayer.find(**options)

    def _get_more(self, cursor, callback):
        """Calls the given callback if there is data available on the cursor.

        Parameters:

        cursor: database cursor returned from a find operation.
        callback: a function to be called back in case of new data.
            callback function should have `response`, `error`,
            and `new` fields. `new` is going to be False.
        """
        # If the client went away,
        # clean up the  cursor and close the connection
        if not self.request.connection.stream.socket:
            self._remove_cursor()
            self.finish()
            return
        # If the cursor is not alive, issue new find to the database
        if cursor and cursor.alive:
            cursor.get_more(callback)
        else:
            callback.keywords["response"] = []
            callback.keywords["error"] = None
            callback.keywords["last_batch"] = True
            callback()

    def _remove_cursor(self):
        """Clean up the opened database cursor."""
        if getattr(self, '_cursor', None):
            del self._cursor

    def _get_on_response(self, response, error, new=False,
                        is_list=False, query=None, last_batch=False):
        """callback for get request

        Parameters:
            response: the response body from the database
            error: any error messages from the database.
            new: True if this is the first time to call this method.
            is_list: If True listing is requered, for example /nodes,
                    otherwise it's a single object like /nodes/node_id
        """
        print "#####RESPONSE", dumps_mongo(response)
        if error:
            self.send_error(500, message=error)
            return
        keep_alive = self.supports_streaming
        if new and not response and not is_list:
            self.send_error(404)
            return
        if response and not is_list:
            response = response[0]
            if response.get("status", None) == "DELETED":
                self.set_status(410)
                self._remove_cursor()
                self.finish()
                return
        cursor = self._get_cursor()
        response_callback = functools.partial(self._get_on_response,
                                    new=False, is_list=is_list)
        get_more_callback = functools.partial(self._get_more,
                                    cursor, response_callback)

        # This will be called when self._get_more returns empty response
        if not new and not response and keep_alive and not last_batch:
            IOLoop.instance().add_callback(get_more_callback)
            return

        accept = self.accept_content_type
        self.set_header("Content-Type",
                    accept + "; profile=" + self.schemas_single[accept])
        if accept == MIME['PSJSON'] or accept == MIME['JSON']:
            json_response = dumps_mongo(response,
                                indent=2).replace('\\\\$', '$').replace('$DOT$', '.')
            # Mongo sends each batch a separate list, this code fixes that
            # and makes all the batches as part of single list
            if is_list:
                if not new and response:
                    json_response = "," + json_response.lstrip("[")
                if not last_batch:
                    json_response = json_response.rstrip("]")
                if last_batch:
                    if not response:
                        json_response = "]"
                    else:
                        json_response += "]"
            else:
                if not response:
                    json_response = ""
            self.write(json_response)
        else:
            # TODO (AH): HANDLE HTML, SSE and other formats
            json_response = dumps_mongo(response,
                                indent=2).replace('\\\\$', '$')
            # Mongo sends each batch a separate list, this code fixes that
            # and makes all the batches as part of single list
            if is_list:
                if not new and response:
                    json_response = "," + json_response.lstrip("[")
                if not last_batch:
                    json_response = json_response.rstrip("]")
                if last_batch:
                    if not response:
                        json_response = "]"
                    else:
                        json_response += "]"
            else:
                if not response:
                    json_response = ""
            self.write(json_response)

        if keep_alive and not last_batch:
            self.flush()
            get_more_callback()            
        else:
            if last_batch:
                self._remove_cursor()
                self.finish()
            else:
                get_more_callback()

    def _validate_psjson_profile(self):
        """
        Validates if the profile provided with the content-type is valid.
        """
        regex = re.compile(".*(?P<p>profile\=(?P<profile>[^\;\ ]*))")
        content_type = self.request.headers.get("Content-Type", "")
        # use the default schema
        if "profile" not in content_type:
            content_type += ";profile=" + \
                self.schemas_single[self.accept_content_type]
        match = re.match(regex, content_type)
        if not match:
            self.send_error(400, message="Bad Content Type '%s'" % content_type)
            return None
        profile = match.groupdict().get("profile", None)
        if not profile:
            self.send_error(400, message="Bad Content Type '%s'" % content_type)
            return None
        if profile != self.schemas_single[self.accept_content_type]:
            self.send_error(400, message="Bad schema '%s'" % profile)
            return None
        return profile

    @tornado.web.asynchronous
    @tornado.web.removeslash
    def post(self, res_id=None):
        # Check if the schema for conetnt type is known to the server
        if self.accept_content_type not in self.schemas_single:
            message = "Schema is not defiend fot content of type '%s'" % \
                        (self.accept_content_type)
            self.send_error(500, message=message)
            return
        # POST requests don't work on specific IDs
        if res_id:
            message = "NetworkResource ID should not be defined."
            self.send_error(400, message=message)
            return

        # Load the appropriate content type specific POST handler
        if self.content_type == MIME['PSJSON']:
            self.post_psjson()
        else:
            self.send_error(500,
                message="No POST method is implemented fot this content type")
            return
        return

    def post_psjson(self):
        """
        Handles HTTP POST request with Content Type of PSJSON.
        """
        profile = self._validate_psjson_profile()
        if not profile:
            return
        try:
            body = json.loads(self.request.body)
        except Exception as exp:
            self.send_error(400, message="malformatted json request '%s'." % exp)
            return
        
        try:
            resources = []
            if isinstance(body, list):
                for item in body:
                    resources.append(self._model_class(item))
            else:
                resources = [self._model_class(body)] 
        except Exception as exp:
            self.send_error(400, message="malformatted request " + str(exp))
            return
        
        # Validate schema
        res_refs =[]
        for index in range(len(resources)):
            try:
                item = resources[index]
                item["selfRef"] = "%s/%s" % \
                    (self.request.full_url(), item[self.Id])
                item["$schema"] = item.get("$schema", self.schemas_single[MIME['PSJSON']])
                item._validate()
                res_ref = {}
                res_ref[self.Id] = item[self.Id]
                res_ref[self.timestamp] = item[self.timestamp]
                res_refs.append(res_ref)
                resources[index] = dict(item._to_mongoiter())
            except Exception as exp:
                self.send_error(400, message="Not valid body '%s'." % exp)
                return
        
        callback = functools.partial(self.on_post,
                    res_refs=res_refs, return_resources=True)
        self.dblayer.insert(resources, callback=callback)

    def on_post(self, request, error=None, res_refs=None, return_resources=True):
        """
        HTTP POST callback to send the results to the client.
        """
        
        if error:
            if isinstance(error, IntegrityError):
                self.send_error(409,
                    message="Could't process the POST request '%s'" % \
                        str(error).replace("\"", "\\\""))
            else:
                self.send_error(500,
                    message="Could't process the POST request '%s'" % \
                        str(error).replace("\"", "\\\""))
            return
        
        if return_resources:
            query = {"$or": []}
            for res_ref in res_refs:
                query["$or"].append(res_ref)
            self.dblayer.find(query, self._return_resources)
        else:
            accept = self.accept_content_type
            self.set_header("Content-Type", accept + \
                " ;profile="+ self.schemas_single[accept])
            if len(res_refs) == 1:
                self.set_header("Location",
                    "%s/%s" % (self.request.full_url(), res_refs[0][self.Id]))
            self.set_status(201)
            self.finish()

    def _return_resources(self, request, error=None):
        unescaped = []
        accept = self.accept_content_type
        self.set_header("Content-Type", accept + \
                " ;profile="+ self.schemas_single[accept])
        self.set_status(201)
        try:
            for res in request:
                unescaped.append(ObjectDict._from_mongo(res))
            
            if len(unescaped) == 1:
                location = self.request.full_url()
                if not location.endswith(unescaped[0][self.Id]):
                    location = location + "/" + unescaped[0][self.Id]
                self.set_header("Location", location)
                self.write(dumps_mongo(unescaped[0], indent=2))
            else:
                self.write(dumps_mongo(unescaped, indent=2))
        except Exception as exp:
            self.send_error(500,
                    message="Could't process the POST request '%s'" % \
                        str(exp).replace("\"", "\\\""))
            return
        self.finish()

    @tornado.web.asynchronous
    @tornado.web.removeslash
    def put(self, res_id=None):
        # Check if the schema for conetnt type is known to the server
        if self.accept_content_type not in self.schemas_single:
            message = "Schema is not defiend fot content of type '%s'" \
                        % self.accept_content_type
            self.send_error(500, message=message)
            return
        # PUT requests only work on specific IDs
        if res_id is None:
            message = "NetworkResource ID is not defined."
            self.send_error(400, message=message)
            return

        # Load the appropriate content type specific PUT handler
        if self.content_type == MIME['PSJSON']:
            self.put_psjson(unicode(res_id))
        else:
            self.send_error(500,
                message="No put method is implemented fot this content type")
            return

    def put_psjson(self, res_id):
        """
        Validates and inserts HTTP PUT request with Content-Type of psjon.
        """
        try:
            body = json.loads(self.request.body)
            resource = self._model_class(body, auto_id=False)
        except Exception as exp:
            self.send_error(400, message="malformatted json request '%s'." % exp)
            return

        if self.Id not in resource:
            resource[self.Id] = res_id
        
        if resource[self.Id] != res_id:
            self.send_error(400,
                message="Different ids in the URL" + \
                 "'%s' and in the body '%s'" % (body[self.Id], res_id))
            return
        
        resource["$schema"] = resource.get("$schema", self.schemas_single[MIME['PSJSON']])
        
        # Validate schema
        try:
            resource._validate()
        except Exception as exp:
            self.send_error(400, message="Not valid body " + str(exp))
            return
        
        res_ref = {}
        res_ref[self.Id] = resource[self.Id]
        res_ref[self.timestamp] = resource[self.timestamp]
        callback = functools.partial(self.on_put, res_ref=res_ref, 
            return_resource=True)
        self.dblayer.insert(dict(resource._to_mongoiter()), callback=callback)

    def on_put(self, response, error=None, res_ref=None, return_resource=True):
        """
        HTTP PUT callback to send the results to the client.
        """
        if error:
            if str(error).find("Integrity") > -1:
                self.send_error(409,
                    message="Could't process the PUT request '%s'" % \
                            str(error).replace("\"", "\\\""))
            else:
                self.send_error(500,
                    message="Could't process the PUT request '%s'" % \
                            str(error).replace("\"", "\\\""))
            return
        
        accept = self.accept_content_type
        profile = self.schemas_single[accept]
        if return_resource:
            query = {"$or": [res_ref]}
            self.dblayer.find(query, self._return_resources)
        else:
            self.set_header("Content-Type", accept + \
                ";profile=" +profile)
            self.set_status(201)
            self.finish()

    def on_connection_close(self):
        self._remove_cursor()
    
    @tornado.web.asynchronous
    @tornado.web.removeslash
    def delete(self, res_id=None):
        # Check if the schema for conetnt type is known to the server
        if self.accept_content_type not in self.schemas_single:
            message = "Schema is not defiend fot content of type '%s'" \
                        % self.accept_content_type
            self.send_error(500, message=message)
            return
        # PUT requests only work on specific IDs
        if res_id is None:
            message = "NetworkResource ID is not defined."
            self.send_error(400, message=message)
            return
        
        self._res_id = unicode(res_id)
        
        self._find({}, callback=self.on_delete)
    
    def on_delete(self, response, error=None):
        if error is not None:
            message = str(error)
            self.send_error(400, message=message)
            return
        if len(response) == 0:
            self.send_error(404)
            return
        deleted = copy.copy(response[0])
        deleted["status"] = "DELETED"
        deleted["ts"] = int(time.time() * 1000000) 
        self.dblayer.insert(deleted, callback=self.finish_delete)
        
    def finish_delete(self, response, error=None):
        if error is not None:
            message = str(error)
            self.send_error(400, message=message)
            return
        self.finish()



class CollectionHandler(NetworkResourceHandler):
    def initialize(self, collections, *args, **kwargs):
        self._collections = collections
        super(CollectionHandler, self).initialize(*args, **kwargs)
        self._models_index = {}
        self._dblayers_index = {}
        self._cache = {}
        for key, value in self._collections.items():
            self._models_index[value["model_class"]] = key
            dblayer = self.application.get_db_layer(value["collection_name"],
                    value["id_field_name"],
                    value["timestamp_field_name"],
                    value["is_capped_collection"],
                    value["capped_collection_size"]
                )
            self._dblayers_index[key] = dblayer
    
    @tornado.web.asynchronous
    @tornado.web.removeslash
    def post(self):
        # Check if the schema for conetnt type is known to the server
        if self.accept_content_type not in self.schemas_single:
            message = "Schema is not defiend fot content of type '%s'" % \
                        (self.accept_content_type)
            self.send_error(500, message=message)
            return
        
        # Load the appropriate content type specific POST handler
        if self.content_type == MIME['PSJSON']:
            self.post_psjson()
        else:
            self.send_error(500,
                message="No POST method is implemented fot this content type")
            return
        return
    
    @gen.engine
    def post_psjson(self):
        """
        Handles HTTP POST request with Content Type of PSJSON.
        """
        profile = self._validate_psjson_profile()
        if not profile:
            return
        try:
            body = json.loads(self.request.body)
        except Exception as exp:
            self.send_error(400, message="malformatted json request '%s'." % exp)
            return
        
        try:
            collections = []
            if isinstance(body, list):
                for item in body:
                    collections.append(self._model_class(item,
                        schemas_loader=schemaLoader))
            else:
                collections = [self._model_class(body,
                        schemas_loader=schemaLoader)] 
        except Exception as exp:
            self.send_error(400, message="malformatted request " + str(exp))
            return
        
        # Validate schema
        try:
            for collection in collections:
                collection._validate()
        except Exception as exp:
            self.send_error(400, message="Not valid body '%s'." % exp)
            return
        
        self._cache = {}
        coll_reps = []
        for collection in collections:
            collection["selfRef"] = "%s/%s" % (self.request.full_url(), collection[self.Id])
                    
            # Convert JSONPath and JSONPointer Links to Hyper Links
            ret = self._complete_href_links(collection, collection)
            # Check if something went wrong
            if ret < 0:
                return
            
            res_refs = [
                {
                    self.Id: collection[self.Id],
                    self.timestamp: collection[self.timestamp]
                }
            ]
            has_error = False
            keys_to_insert = []
            http_client = AsyncHTTPClient()
            
            # Async calls to insert all the resources included in the request
            responses = yield [
                gen.Task(
                    http_client.fetch,
                    "%s://%s%s" % (self.request.protocol, self.request.host, self.reverse_url(key)),
                    method = "POST",
                    body = dumps_mongo(collection[key]),
                    headers = {
                        "Cache-Control": "no-cache",
                        "Content-Type": MIME['PSJSON'],
                        "Connection": "close"
                        }
                    )
                    for key in self._collections.keys()
                    if key in collection
            ]
            
            for response in responses:
                if response.code >= 400:
                    self.send_error(response.code, message=response.body)
                    return
           
            for key in self._collections:
                if key not in collection:
                    continue
                for index in range(len(collection[key])):
                    collection[key][index] = {"href": collection[key][index]["selfRef"], "rel": "full"}
            coll_reps.append(dict(collection._to_mongoiter()))
        
        callback = functools.partial(self.on_post, res_refs=res_refs)
        self.dblayer.insert(coll_reps, callback=callback)
            

    def set_self_ref(self, resource):
        """Assignes a selfRef to a resource"""
        fullname = utils.class_fullname(resource)
        if fullname not in self._models_index:
            self.send_error(400,
                message="Unrecognized resource type: %s" % type(resource))
            return -1
        resource_name = self._models_index[fullname]
        resource_url = self.reverse_url(
            self._collections[resource_name]["name"], resource[self.Id]) 
        resource["selfRef"] = "%s://%s%s" % (
            self.request.protocol, self.request.host, resource_url)
        return 0
            
    def _complete_href_links(self, parent_collection, current):
        """Resolves self hyperlinks (JSONPath and JSONPointers."""
        if isinstance(current, HyperLink) or \
            (isinstance(current, dict) and "href" in current):
            if isinstance(current["href"], (unicode, str)):
                resource = None
                if current["href"] in self._cache:
                    resource = self._cache[current["href"]]
                elif current["href"].startswith("#"):
                    resource = jsonpointer.resolve_pointer(parent_collection,
                              current["href"][1:])
                    if not resource:
                        resource = "Unresolved"
                elif current["href"].startswith("$"):
                    path = jsonpath(parent_collection,
                        current["href"], result_type="PATH")
                    if path:
                        resource = eval("parent_collection%s" % path[0].lstrip("$"))
                    else:
                        resource = "Unresolved"
                self._cache[current["href"]] = resource
                if resource and resource != "Unresolved":
                    if "selfRef" not in resource:
                        ret = self.set_self_ref(resource)
                        if ret < 0:
                            return ret
                    current["href"] = resource["selfRef"]
            return 0
        elif isinstance(current, list):
            keys = range(len(current))
        elif isinstance(current, dict):
            keys = current.keys()
        else:
           return 0
        
        for key in keys:
            value = current[key]
            if isinstance(value, (NetworkResource, Topology)) and \
                "selfRef" not in value:
                ret = self.set_self_ref(value)
                if ret < 0:
                    return ret
            if isinstance(value, list) or isinstance(value, dict):
                ret = self._complete_href_links(parent_collection, value)
                if ret < 0:
                    return ret
        return 0


class MainHandler(tornado.web.RequestHandler):
    def initialize(self, base_url, resources):
        self._resources = resources
    
    def get(self):
        links = []
        for resource in self._resources:
            href = "%s://%s%s" % (self.request.protocol,
                self.request.host, self.reverse_url(resource))
            links.append({"href": href, "rel": "full"})
        self.set_header("Content-Type", MIME["JSON"])
        self.write(json.dumps(links, indent=4))

 
              
class EventsHandler(NetworkResourceHandler):        
        
    @tornado.web.asynchronous
    @tornado.web.removeslash
    def post(self, res_id=None):
        # Check if the schema for conetnt type is known to the server
        if self.accept_content_type not in self.schemas_single:
            message = "Schema is not defiend fot content of type '%s'" % \
                        (self.accept_content_type)
            self.send_error(500, message=message)
            return
        # POST requests don't work on specific IDs
        if res_id:
            message = "NetworkResource ID should not be defined."
            self.send_error(400, message=message)
            return

        # Load the appropriate content type specific POST handler
        if self.content_type == MIME['PSJSON']:
            self.post_psjson()
        else:
            self.send_error(500,
                message="No POST method is implemented fot this content type")
            return
        return

    def on_post(self, request, error=None, res_refs=None, return_resources=True, last=True):
        """
        HTTP POST callback to send the results to the client.
        """
        
        if error:
            if isinstance(error, IntegrityError):
                self.send_error(409,
                    message="Could't process the POST request '%s'" % \
                        str(error).replace("\"", "\\\""))
            else:
                self.send_error(500,
                    message="Could't process the POST request '%s'" % \
                        str(error).replace("\"", "\\\""))
            return                
        self.set_status(201)
        self.finish()
           
                    
    def verify_metadata(self,response, collection_size,post_body):
        if response.error:
            self.send_error(400, message="metadata is not found '%s'." % response.error)
        else:
            body=json.loads(response.body)
            if body["id"] not in self.application.sync_db.collection_names():
                self.application.get_db_layer(body["id"],"id","ts",True,collection_size)
                self.set_header("Location",
                    "%s/data/%s" % (self.request.full_url(), body["id"]))
                callback = functools.partial(self.on_post,
                                             res_refs=None, return_resources=True)
                self.dblayer.insert(post_body, callback=callback)
            else:
                self.send_error(401, message="event collection exists already")  
            
    def post_psjson(self):
        """
        Handles HTTP POST request with Content Type of PSJSON.
        """
        profile = self._validate_psjson_profile()
        if not profile:
            return
        try:
            body = json.loads(self.request.body)
        except Exception as exp:
            self.send_error(400, message="malformatted json request '%s'." % exp)
            return
        

        callback = functools.partial(self.verify_metadata,
                                     collection_size=body["collection_size"], post_body=body)
        
        http_client = AsyncHTTPClient()
        http_client.fetch(body["metadata_URL"], callback)        

    def del_stat_fields(self,generic):
        del generic["ns"]
        del generic["numExtents"]
        del generic["nindexes"]
        del generic["lastExtentSize"]
        del generic["paddingFactor"]
        del generic["flags"]
        del generic["totalIndexSize"]
        del generic["indexSizes"]
        del generic["max"]
        del generic["ok"]
        if generic["capped"] == 1:
            generic["capped"]="Yes"
        else:
            generic["capped"]="No"

       
    def generate_response(self,query,mid,response,index):
        try:
            command={"collStats":mid,"scale":1}
            generic = self.application.sync_db.command(command)
        except Exception as exp:
            self.send_error(400, message="At least one of the metadata ID is invalid.")
            return
              
        self.del_stat_fields(generic)
        specific={}
        if 'ts' in self.request.arguments.keys():       
            criteria=self.request.arguments['ts'][0].split('=')
            
            if criteria[0]=='gte':
                specific["startTime"]=int(criteria[1])
            if criteria[0]=='lte':
                specific["endTime"]=int(criteria[1])
            
            if self.request.arguments['ts'].__len__() > 1 :            
                criteria=self.request.arguments['ts'][1].split('=')
                if criteria[0]=='gte':
                    specific["startTime"]=int(criteria[1])
                if criteria[0]=='lte':
                    specific["endTime"]=int(criteria[1])
            
            db_query=copy.deepcopy(query)
            del db_query["$and"][index]
            specific["numRecords"]=self.application.sync_db[mid].find(db_query).count()
            
        response.insert(0,{})
        response[0]["mid"]=mid
        response[0]["generic"]=generic
        response[0]["queried"]=specific

                                            
    @tornado.web.asynchronous
    @tornado.web.removeslash
    def get(self, res_id=None):
        """Handles HTTP GET"""
        accept = self.accept_content_type
        if res_id:
            self._res_id = unicode(res_id)
        else:
            self._res_id = None
            
        parsed = self._parse_get_arguments()
        #print self.application.sync_db.command({"collStats":"4fdf07de1d41c82375000000","scale":1})
        query = parsed["query"]
        fields = parsed["fields"]
        limit = parsed["limit"]
        is_list = not res_id
#        len=query['$and'].__len__()
        if query.__len__() == 0:
            print query;
            cursor =  self.application.sync_db["events_cache"].find()
            index = -1
            response = []
            obj = next(cursor,None)
            while obj:
                index = index+1
                mid = obj["metadata_URL"].split('/')[obj["metadata_URL"].split('/').__len__() - 1]
                self.generate_response(query,mid,response,index)
                obj = next(cursor, None)
            try:
                json_response = json.dumps(response,cls=MongoEncoder, indent=2)
                self.write(json_response)
                self.finish()
            except Exception as exp:
                self.send_error(400, message="1 At least one of the metadata ID is invalid.")
                return                
        else:
            index=-1
            response=[]
            for d in query["$and"]:
                index=index+1
                if 'mids' in d.keys():
                    if isinstance(d["mids"],dict):
                        for m in d['mids']['$in']:
                            self.generate_response(query,m,response,index)
                    else:
                        self.generate_response(query,d['mids'],response,index)
            try:
                json_response = json.dumps(response,cls=MongoEncoder, indent=2)
                self.write(json_response)
                self.finish()
            except Exception as exp:
                self.send_error(400, message="1 At least one of the metadata ID is invalid.")
                return                
        
class DataHandler(NetworkResourceHandler):        
        
    @tornado.web.asynchronous
    @tornado.web.removeslash
    def post(self, res_id=None):
        # Check if the schema for conetnt type is known to the server
        if self.accept_content_type not in self.schemas_single:
            message = "Schema is not defiend fot content of type '%s'" % \
                        (self.accept_content_type)
            self.send_error(500, message=message)
            return
        # POST requests don't work on specific IDs
        #if res_id:
        #    message = "NetworkResource ID should not be defined."
        #    self.send_error(400, message=message)
        #    return
        self._res_id=res_id
        #Load the appropriate content type specific POST handler
        if self.content_type == MIME['PSJSON']:
            self.post_psjson()
        else:
            self.send_error(500,
                message="No POST method is implemented fot this content type")
            return
        return
    
    def on_post(self, request, error=None, res_refs=None, return_resources=True, last=True):
        """
        HTTP POST callback to send the results to the client.
        """
        
        if error:
            if isinstance(error, IntegrityError):
                self.send_error(409,
                    message="Could't process the POST request '%s'" % \
                        str(error).replace("\"", "\\\""))
            else:
                self.send_error(500,
                    message="Could't process the POST request '%s'" % \
                        str(error).replace("\"", "\\\""))
            return
        
        if return_resources:
            query = {"$or": []}
            for res_ref in res_refs:
                query["$or"].append(res_ref)
            self.dblayer.find(query, self._return_resources)
        else:
            if last:
                accept = self.accept_content_type
                self.set_header("Content-Type", accept + \
                                " ;profile="+ self.schemas_single[accept])
                if len(res_refs) == 1:
                    self.set_header("Location",
                                    "%s/%s" % (self.request.full_url(), res_refs[0][self.Id]))
                
                self.set_status(201)
                self.finish()   
                     
    def post_psjson(self):
        """
        Handles HTTP POST request with Content Type of PSJSON.
        """                    
        profile = self._validate_psjson_profile()
        if not profile:
            return
        try:
            body = json.loads(self.request.body)
        except Exception as exp:
            self.send_error(400, message="malformatted json request '%s'." % exp)
            return
        if self._res_id:
            res_refs =[]
            if self._res_id in self.application.sync_db.collection_names():
                callback = functools.partial(self.on_post,
                        res_refs=res_refs, return_resources=False,last=True)
                self.application.async_db[self._res_id].insert(body["data"], callback=callback)
            else:
                self.send_error(400, message="The collection for this metadata ID does not exist")
                return
        else:
            for i in range(0,body.__len__()):
                mid = body[i]['mid']
                data = body[i]['data']
                res_refs =[]
                if body[i]['mid'] in self.application.sync_db.collection_names():
                    if i+1 == body.__len__() :
                        callback = functools.partial(self.on_post,
                                                     res_refs=res_refs, return_resources=False,last=True)
                        self.application.async_db[mid].insert(data, callback=callback)
                    else :
                        callback = functools.partial(self.on_post,
                                                     res_refs=res_refs, return_resources=False,last=False)
                        self.application.async_db[mid].insert(data, callback=callback)
                    
                else:
                    self.send_error(400, message="The collection for this metadata ID does not exist")
                    return

    @tornado.web.asynchronous
    @tornado.web.removeslash
    def get(self, res_id=None):
        """Handles HTTP GET"""
        accept = self.accept_content_type
        if res_id:
            self._res_id = unicode(res_id)
        else:
            self.send_error(500, message="You need to specify the metadata ID in the URL while querying the data")
            return
        
        parsed = self._parse_get_arguments()
        query = parsed["query"]
        fields = parsed["fields"]
        fields["_id"] = 0
        limit = parsed["limit"]
        is_list = True #, not res_id
        if query:
            is_list = True
        callback = functools.partial(self._get_on_response,
                            new=True, is_list=is_list, query=query)
        self._find(query, callback, fields=fields, limit=limit)

    def _find(self, query, callback, fields=None, limit=None):
        """Query the database.

        Parameters:

        callback: a function to be called back in case of new data.
                callback function should have `response`, `error`,
                and `new` fields. `new` is going to be True.
        """
        keep_alive = self.supports_streaming or self.supports_sse()
        if self._res_id:
            query[self.Id] = self._res_id
        options = dict(query=query, callback=callback)#, await_data=True)
        # Makes it a tailable cursor
        if keep_alive and self._tailable:
            options.update(dict(tailable=True, timeout=False))
        if fields:
            options["fields"] = fields
        if limit:
            options["limit"] = limit
        if "sort" not in options:
            options["sort"] = []
        options["sort"].append(("ts", -1))
        self._query = query
        db_layer = self.application.get_db_layer(self._res_id, "_id", "ts",
                        True,  5000)
        query.pop("id", None)
        self._cursor = db_layer.find(**options)        
