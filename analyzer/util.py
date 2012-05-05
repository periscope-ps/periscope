"""
Utility functions for Web.py backend
"""
__rcsid__ = "$Id: util.py 29859 2012-02-01 23:36:09Z dang $"

# standard includes
import os
import re
# third-party includes
import json
import pystache
from pystache import loader
import web

"""
Expected format for UUID is:
    77D2E619-41C5-42C6-8C55-2CF54EF30F04
"""
UUID_RE = re.compile(
    "{0}{{8}}-{0}{{4}}-{0}{{4}}-{0}{{4}}-{0}{{12}}"
    .format("[0-9A-Fa-f]"))

def is_valid_uuid(u):
    """Check for valid UUID.
    Returns:
       True or False
    """
    return bool(UUID_RE.match(u))

def split_uuids(s):
    """Split the '/' separated path of UUIDs

    Params:
      s - String from request, not url-encoded, with no leading '/'
    Returns:
      List of UUIDs
    Raises:
      ValueError if path is empty or contains invalid UUIDs

    Sample usage:
    >>> get_wf_path("77D2E619-41C5-42C6-8C55-2CF54EF30F04/52932F08-15B0-4072-A8EB-18B8F09DCE7E")
    ['77D2E619-41C5-42C6-8C55-2CF54EF30F04', '52932F08-15B0-4072-A8EB-18B8F09DCE7E']

    """
    result = s.split("/")
    for uuid in result:
        if not is_valid_uuid(uuid):
            raise ValueError("invalid UUID: {0}".format(uuid))
    return result

def json_header():
    "Add JSON header."
    web.header('Content-Type', 'text/json') 

def returns_json(fn):
    """Decorator to add headers and convert
       Python dict to JSON string before returning it.
    """
    def new(self, *args, **kwarg):
        json_header()
        json_data = json.dumps(fn(self, *args, **kwarg))
        #print("RETURN: "+json_data) # debug
        return json_data
    return new

class BaseLocalView:
    def __init__(self, **kw):
        self._static = "/static/"

if hasattr(pystache, 'View'):
    class LocalView(pystache.View, BaseLocalView):
        def __init__(self, **kw):
            pystache.View.__init__(self, **kw)
            BaseLocalView.__init__(self)
        def js_path(self): return self._static + "js"
        def img_path(self): return self._static + "img"
        def css_path(self): return self._static + "css"
        def html_path(self): return self._static + "html"
else:
    class LocalView(BaseLocalView):
        def __init__(self, **kw):
            BaseLocalView.__init__(self)
            self._loader = None
            self._context = kw
            for ext in "js", "img", "css", "html":
                self._context[ext + "_path"] = self._static + ext
        def render(self):
            if self._loader is None:
                self._loader = loader.Loader(search_dirs=[self.template_path])
            tmpl = self._loader.load_name(self.template_name)
            r = pystache.Renderer(search_dirs=[self.template_path])
            return r.render(tmpl, self._context)

class render(object):
    """Make pystache rendering imitate web.py native
    rendering function.

    Usage: x = render("path/to/templates/")
    x.<name>(var1=value, ..)
    where <name> is then matched to path/to/templates/<name>.mustache

    """
    def __init__(self, base_dir):
        self._dir = base_dir

    def __getattr__(self, key):
        #print("GET ATTR: "+key)
        if not key.startswith("_"):
            def render_fn(**kw):
                view = LocalView(**kw)
                view.template_path = self._dir
                view.template_name = key
                try:
                    result = view.render()
                except IOError, err:
                    raise ValueError("Template {name:s} not found: {msg:s}"
                    .format(name=key, msg=err))
                web.header('Content-Type', 'text/html')
                return result
            return render_fn
        else:
            return self.__dict__[key]
