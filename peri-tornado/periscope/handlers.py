#!/usr/bin/env python
"""
Periscope HTTP(s) Handlers.
"""

import json
import re
import functools
from netlogger import nllog
from tornado.ioloop import IOLoop
import tornado.web
from tornado.httpclient import HTTPError
from pymongo.objectid import ObjectId
from periscope.models import DBLayer
from periscope.models import MongoEncoder
from asyncmongo.errors import IntegrityError
MIME = {
    'HTML': 'text/html',
    'JSON': 'application/json',
    'PLAIN': 'text/plain',
    'SSE': 'text/event-stream',
    'PSJSON': 'application/perfsonar+json',
    'PSXML': 'application/perfsonar+xml',
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
                    "time is %d\n last event id was %s" %
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

        At the fist look it might look weird to have all function paramters
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

    def initialize(self, collection_name, base_url,
            schemas_single=None,
            schemas_list=None,
            allow_get=False,
            allow_post=True,
            allow_put=True,
            allow_delete=True,
            tailable=False,
            accepted_mime=[MIME['SSE'], MIME['PSJSON'], MIME['PSXML'], MIME['HTML']]):
        """
        Initializes handler for certain type of network resources.

        Parameters:
        collection_name: name of the database collection name that
                        stores information about the network resource.
        base_url: the base the path to access this resource, e.g., /nodes
        schemas_single: a dictionary that represents the network resources schema
                        to be validated againest. The dictionary is indexed
                        by content-type.
        schemas_list: a dictionary that represents the listing of this resources
                        schema to be validated againest.
        allow_get: User client can issue HTTP GET requests to this resource
        allow_post: User client can issue HTTP POST requests to this resource
        allow_put: User client can issue HTTP PUT requests to this resource
        allow_delete: User client can issue HTTP DELETE requests to this resource
        tailable: The underlying database collection is a capped collection
        """
        
        # TODO (AH): Add ability to define the JSON schema for the resource
        # TODO (AH): Add ability to Enable/Disable different HTTP methods
        # TODO (AH): Add ability to Enable/Disable different Content Types
        self._collection_name = collection_name
        self._base_url = base_url
        self._schemas_single = schemas_single 
        self._schemas_list = schemas_list
        self._allow_get = allow_get
        self._allow_post= allow_post
        self._allow_put = allow_put
        self._allow_delete = allow_delete
        self._accepted_mime = accepted_mime
        if tailable and tailable:
            raise ValueError("Capped collections do not support delete operations")
        self._collection = self.application.async_db[collection_name]
        self._dblayer = DBLayer(self._collection)
        
    @property
    def model(self):
        """Returns a reference to the DB Layer."""
        if not getattr(self, "_dblayer", None):
            raise TypeError("No DB layer is defined for this handler.")
        return self._dblayer

    def _get_accept_content_type(self):
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
            accept = self.request.headers.get("Accept", MIME['PSJSON']).split(",")
            for accepted_mime in self._accepted_mime:
                if accepted_mime in accept:
                    self._accept = accepted_mime
            if "*/*" in accept:
                self._accept = MIME['PSJSON']
            if not self._accept:
                raise HTTPError(406, "Unsupported accept content type '%s'" % self.request.headers.get("Accept", None))
        return self._accept

    def _get_content_type(self):
        """
        Returns the content type of the client's request

        See:
            http://www.w3.org/Protocols/rfc2616/rfc2616-sec12.html
            http://www.ietf.org/rfc/rfc2295.txt
            http://httpd.apache.org/docs/2.2/content-negotiation.html
            http://www.w3.org/TR/webarch/#def-coneg
        """
        if not getattr(self, '_content_type', None):
            content_type = self.request.headers.get("Content-Type", MIME['PSJSON']).split(",")
            for accepted_mime in self._accepted_mime:
                if accepted_mime in content_type:
                    self._content_type = accepted_mime
                    return self._content_type
            raise HTTPError(415, "Unsupported content type '%s'" % self.request.headers.get("Content-Type", None))
        return self._content_type

    def _supports_streaming(self):
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

    def _parse_get_arguments(self):
        """Parses the HTTP GET areguments given by the user."""
        query = self.request.query
        return query

    def _get_cursor(self):
        """Returns reference to the database cursor."""
        return self._cursor

    @tornado.web.asynchronous
    @tornado.web.removeslash
    def get(self, res_id=None, kwpath=None):
        #self._get_content_type()
        self._get_accept_content_type()
        self._query = {}
        self._fields = {'_id': 0}
        dot_query = None
        if kwpath:
            kwpath = kwpath.strip('/')
            kwpath = kwpath.replace(".", "\\.")
            kwpath = kwpath.replace("$", "\\\\$")
        if res_id:
            self._query['id'] = unicode(res_id)
        if kwpath and res_id:
            dot_query = ".".join(kwpath.split("/"))
            self._query[str(dot_query)] = {"$exists": 1}
        is_list = not res_id
        callback = functools.partial(self._get_on_response,
                            new=True, is_list=is_list, dot_query=dot_query)
        self._find(callback)

    def _find(self, callback):
        """Query the database.

        Parameters:

        callback: a function to be called back in case of new data.
                callback function should have `response`, `error`,
                and `new` fields. `new` is going to be True.
        """

        keep_alive = self._supports_streaming() or self.supports_sse()
        options = dict(query=self._query, callback=callback, fields=self._fields)
        # Makes it a tailable cursor
        if keep_alive:
            options.update(dict(tailable=True, await_data=True, timeout=False))
        self._cursor = self.model.find(**options)

    def _get_more(self, cursor, callback):
        """Calls the given callback if there is data available on the cursor.

        Parameters:

        cursor: database cursor returend from a find operation.
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
            self.finish()
            self._find(callback)

    def _remove_cursor(self):
        """Clean up the opened database cursor."""
        if getattr(self, '_cursor', None):
            del self._cursor

    def _get_on_response(self, response, error, new=False, is_list=False, dot_query=None):
        """callback for get request

        Parameters:
            response: the response body from the database
            error: any error messages from the database.
            new: True if this is the first time to call this method.
            is_list: If True listing is requered, for example /nodes,
                    otherwise it's a single object like /nodes/node_id
        """
        if error:
            self.send_error(500, error)
            return
        keep_alive = self._supports_streaming()

        if new and not response and not is_list:
            self.send_error(404)
            return
        if response and not is_list:
            response = response[0]
        r = response
        # Filters the dot query such that only the result is returned to the user
        if dot_query:
            fields = dot_query.split(".")
            for index in range(len(fields)):
                # if the filterd field is a list
                if isinstance(response, list):
                    response = response[int(fields[index])]
                else:
                    response = response[fields[index]]

        cursor = self._get_cursor()
        response_callback = functools.partial(self._get_on_response,
                                    new=False, is_list=is_list)
        get_more_callback = functools.partial(self._get_more,
                                    cursor, response_callback)

        # This will be called when self._get_more returns empty response
        if not new and not response and keep_alive:
            IOLoop.instance().add_callback(get_more_callback)
            return

        accept = self._get_accept_content_type()
        self.set_header("Content-Type", accept)
        
        if accept == MIME['PSJSON']:
            self.write(json.dumps(response, cls=MongoEncoder).replace('\\\\$', '$'))
        else:
            # TODO (AH): HANDLE HTML, SSE and other formats
            self.write(json.dumps(response, cls=MongoEncoder).replace('\\\\$', '$'))
            pass
        if keep_alive:
            self.flush()
            IOLoop.instance().add_callback(get_more_callback)
        else:
            self._remove_cursor()
            self.finish()

    @tornado.web.asynchronous
    def post(self, res_id=None, kwpath=None):
        self._get_content_type()
        self._get_accept_content_type()
        callback = functools.partial(self._do_post)
        self._validate_post(res_id, kwpath, callback)

    def _validate_post(self, res_id, kwpath, callback):
        # Escape special characters
        body = self.request.body.replace("$", "\\\\$")
        json_body = json.loads(body)
        insert = False
        if not res_id and not kwpath:
            insert = True
            if not json_body.get('id', None):
                json_body['id'] = unicode(ObjectId())
            res_id = json_body['id']        
        callback2 = functools.partial(callback, res_id=res_id, insert=insert)
        query = []
        if kwpath:
            kwpath = kwpath.strip('/')
            kwpath = kwpath.replace(".", "\\.")
            kwpath = kwpath.replace("$", "\\\\$")
        query = {'id': res_id}
        if kwpath:
            data = {
                "$set": {".".join(kwpath.split("/")): json_body}
            }
        else:
            data = json_body
        callback2(query=query, data=data)

    def _do_post(self, query, data, res_id=None, insert=True):
        callback = functools.partial(self._on_post_response, res_id=res_id)
        if insert:
            self.model.insert(data, callback)
        else:
            self.model.update(query, data, callback)

    def _on_post_response(self, response, error, res_id):
        if error:
            if isinstance(error, IntegrityError):
                self.send_error(409)
            else:
                self.send_error(500)
            return
        self.set_header("Content-Type", MIME['PSJSON'])
        self.set_status(202)
        if self.request.uri.startswith("https://"):
            protocol = "https://"
        else:
            protocol = "http://"
        self.set_header("Location", "%s%s%s/%s" % (protocol, self.request.host, self._base_url, res_id))
        self.finish()

    def on_connection_close(self):
        self._remove_cursor()
