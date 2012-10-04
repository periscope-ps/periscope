#!/usr/bin/env python
"""
Database models.
"""
import copy
import time
from json import JSONEncoder
import pymongo

if pymongo.__dict__['version'] > '2.2' :
    from bson.objectid import ObjectId
else :
    from pymongo.objectid import ObjectId

import json
import time
import re
import validictory
import functools
import httplib2
from periscope.utils import json_schema_merge_extends
from settings import JSON_SCHEMAS_ROOT

SCHEMAS = {
    'networkresource': 'http://unis.incntre.iu.edu/schema/20120709/networkresource#',
    'node': 'http://unis.incntre.iu.edu/schema/20120709/node#',
    'domain': 'http://unis.incntre.iu.edu/schema/20120709/domain#',
    'port': 'http://unis.incntre.iu.edu/schema/20120709/port#',
    'link': 'http://unis.incntre.iu.edu/schema/20120709/link#',
    'network': 'http://unis.incntre.iu.edu/schema/20120709/network#',
    'topology': 'http://unis.incntre.iu.edu/schema/20120709/topology#',
    'service': 'http://unis.incntre.iu.edu/schema/20120709/service#',
    'path': 'http://unis.incntre.iu.edu/schema/20120709/path#',
    'blipp': 'http://unis.incntre.iu.edu/schema/20120709/blipp#',
    'metadata': 'http://unis.incntre.iu.edu/schema/20120709/metadata#',
    'data' : 'http://unis.incntre.iu.edu/schema/20120709/data#',
    'datum' : 'http://unis.incntre.iu.edu/schema/20120709/datum#',
}


class HyperLinkNotFound(Exception):
    pass


class DeserializationException(Exception):
    pass


class ObjectDict(dict):
    """Extends the dict object to make it's keys accessible via obi.key."""
    
    __special_properties_names__ = [
        "_schema_data",
        "_set_defaults",
        "_validate",
        "_value_converter",
        "__doc__",
    ]
    
    def __init__(self, data=None, _set_attributes=True, schemas_loader=None):
        """
        Initialize new ObjectDict object.
        
        Parameters:
        
        data: initial data in the dict.
        """
        assert isinstance(schemas_loader, (SchemasLoader, type(None))), \
            "schemas_loader is not of type Schemas or None."
        setattr(self, "_$schemas_loader", schemas_loader)
        data = data or {}
        super(ObjectDict, self).__init__(data)
        if _set_attributes:
            for key, value in data.iteritems():
                if not hasattr(self, key):
                    self._add_property(key)
                self._set_property(key, value)
    
    def _add_property(self, name, doc=None):
        """Add a property to the class definition.
        
        name: the name of property.
        
        doc: documenation of the property to be read from obj.name.__doc__.
        """
        fget = lambda self: self._get_property(name)
        fset = lambda self, v: self._set_property(name, v)
        fdel = lambda self: self._del_property(name)
        setattr(self.__class__, name, property(fget, fset, fdel, doc=doc))
    
    def _get_property(self, name):
        """Returns the value of a property."""
        return self.get(name, None)
    
    def _set_property(self, name, value):
        """Set the value of a property."""
        value = self._value_converter(value, name)
        super(ObjectDict, self).__setitem__(name, value)
        
    def _del_property(self, name):
        """Delete a propety."""
        if name in self:
            super(ObjectDict, self).__delitem__(name)
        delattr(self.__class__, name)
    
    def __setattr__(self, name, value):
        if name not in self.__class__.__special_properties_names__ and \
            not name.startswith("_$"):
                if not hasattr(self, name):
                    self._add_property(name)
                value = self._value_converter(value, name)
        super(ObjectDict, self).__setattr__(name, value)
    
    def __setitem__(self, name, value):
        self.__setattr__(name, value)
    
    def __delitem__(self, name):
        self._del_property(name)
    
    def __iter__(self):
        for key in self.iterkeys():
            yield key
    
    def iteritems(self):
        for key in self.iterkeys():
            yield key, self[key]
    
    def itervalues(self):
        for key in self.iterkeys():
            yield self[key]
    
    def _to_mongoiter(self):
        """Escapes mongo's special characters in the keys."""
        for key, value in self.iteritems():
            if isinstance(key, (str, unicode)):
                key = key.replace(".", "$DOT$")
                if key.startswith("$"):
                    key = "\\" + key
            if hasattr(value, "_to_mongoiter"):
                value = dict(value._to_mongoiter())
            if isinstance(value, list):
                for index in range(len(value)):
                    if hasattr(value[index], "_to_mongoiter"):
                        value[index] = dict(value[index]._to_mongoiter())
            yield key, value
    
    @classmethod
    def _from_mongo(cls, data, schemas_loader=None):
        assert isinstance(data, dict)
        tmp = {}
        for key, value in data.iteritems():
            if isinstance(key, (str, unicode)):
                key = key.replace("$DOT$", ".")
                if key.startswith("\\$"):
                    key = key.lstrip("\\")
            if hasattr(value, "_from_mongo"):
                value = value._from_mongo(schemas_loader=schemas_loader)
            elif isinstance(value, dict):
                if "$schema" in value and schemas_loader:
                    obj_cls = schemas_loader.get_class(value["$schema"])
                else:
                    obj_cls = ObjectDict
                value = obj_cls._from_mongo(value, schemas_loader=None)
            elif isinstance(value, list):
                for index in range(len(value)):
                    if isinstance(value[index], dict):
                        value[index] = cls._from_mongo(value[index])
            tmp[key] = value
        return cls(tmp)
    
    def _value_converter(self, value, name=None):
        """Make sure thay properties that have dict values are also returend
        as ObjectDict instance."""
        original_type = type(value)
        if type(value) is list:
            for index in range(len(value)):
                if hasattr(value, "_value_converter"):
                    continue
                original_type = type(value[index])
                new_value = self._value_converter(value[index], None)
                if original_type != type(new_value):
                    value[index] = new_value
        elif type(value) is dict and not hasattr(value, "_value_converter"):
            cls = ObjectDict
            loader = getattr(self, "_$schemas_loader", None)
            if not loader:
                cls = ObjectDict
            elif "$schema" in value:
                cls = loader.get_class(value["$schema"])
            elif "href" in value:
                cls = loader.get_class("http://json-schema.org/draft-03/links#")
            
            if issubclass(cls, JSONSchemaModel):
                value = cls(value,
                    set_defaults=getattr(self, "_set_defaults", True),
                    schemas_loader=getattr(self, "_$schemas_loader"))
            elif issubclass(cls, ObjectDict):
                value = cls(value,
                    schemas_loader=getattr(self, "_$schemas_loader"))
            else:
                value = cls(value)
            if name and original_type != type(value):     
                self._set_property(name, value)
        return value


def schemaMetaFactory(name, schema, extends=None):
    assert isinstance(schema, dict), "schema is not of type dict."
    parent = extends or type
    
    class SchemaMetaClass(parent):
        def __new__(meta, classname, bases, classDict):
            def make_property(name, doc=None):
                fget = lambda self: self._get_property(name)
                fset = lambda self, v: self._set_property(name, v)
                fdel = lambda self: self._del_property(name)
                return  property(fget, fset, fdel, doc=doc)
            
            newtype = super(SchemaMetaClass, meta).__new__(meta, classname, bases, classDict)
            if "description" in schema:
                setattr(newtype, '__doc__', schema["description"])
            if 'properties' not in schema:
                schema['properties'] = {}
            if schema.get("type", "object") == "object":
                for prop, value in schema['properties'].items():
                    if prop not in classDict:
                        doc = value.get("description", None)
                        setattr(newtype, prop, make_property(prop, doc))
            
            setattr(newtype, '_schema_data', schema)
            return newtype
    return SchemaMetaClass


class JSONSchemaModel(ObjectDict):
    """Creates a class type based on JSON Schema."""
    
    def __init__(self, data=None, set_defaults=True, schemas_loader=None):
        """
        Parameters:
        
        schema: dict of the JSON schema to create the class based on.
        
        data: initial data
        
        set_defaults: (optional) if a property has default value on the schema
            then set the value of the attribute to it.
        """
        assert isinstance(data, (dict, type(None))), \
            "data is not of type dict or None."
        assert isinstance(set_defaults, (bool, type(None))), \
            "set_defaults is not of type bool."
        assert isinstance(schemas_loader, (SchemasLoader, type(None))), \
            "schemas_loader is not of type Schemas or None."
        
        data = data or {}
        dict.__init__(self, data)
        
        self._set_defaults =  set_defaults
        setattr(self, "_$schemas_loader", schemas_loader)
        
        for key, value in data.iteritems():
            if not hasattr(self, key):
                prop_type = self._get_property_type(key) or {}
                doc = prop_type.get("description", None)
                self._add_property(key, doc)
            self._set_property(key, value)
    
    def _set_property(self, name, value):
        """Set the value of a property."""
        value = self._value_converter(value, name)
        dict.__setitem__(self, name, value)
    
    def __setattr__(self, name, value):
        if name not in self.__class__.__special_properties_names__ and \
            not name.startswith("_$"):
                if not hasattr(self, name):
                    doc = None
                    # Try to find if there is any doc in the pattern props
                    for pattern, val in self._schema_data.get(
                        "patternProperties", {}).items():
                        if re.match(pattern, name):
                            doc = val.get("description", None)
                    self._add_property(name, doc)
                value = self._value_converter(value, name)
        super(JSONSchemaModel, self).__setattr__(name, value)
    
    def __setitem__(self, name, value):
        self.__setattr__(name, value)
    
    def _get_property_type(self, name):
        if name in self._schema_data["properties"]:
            return self._schema_data["properties"][name]
        for pattern, value in self._schema_data.get("patternProperties", {}).items():
            if re.match(pattern, name):
                return value
        return None
    
    def _value_converter(self, value, prop_name=None):
        """Make sure thay properties that have dict values are also returend
        as ObjectDict instance."""
        original_type = type(value)
        if isinstance(value, list):
            for index in range(len(value)):
                original_type = type(value[index])
                new_value = self._value_converter(value[index], None)
                if original_type != type(new_value):
                    value[index] = new_value        
        elif isinstance(value, dict) and not isinstance(value, ObjectDict):
            cls = ObjectDict
            loader = getattr(self, "_$schemas_loader", None)
            if not loader:
                cls = ObjectDict
            elif "$schema" in value:
                cls = loader.get_class(value["$schema"])
            elif "href" in value:
                cls = loader.get_class("http://json-schema.org/draft-03/links#")
            elif prop_name:
                prop_type = (self._get_property_type(prop_name) or \
                    {}).get("type", None)
                if isinstance(prop_type, list):
                    # TODO (AH): this is very bad to assume the first type
                    prop_type = prop_type[0]
                if type(prop_type) is dict:
                    prop_type = prop_type.get("$ref", None)
                else:
                    prop_type = None
                if prop_type:
                    cls = loader.get_class(prop_type)
            if issubclass(cls, JSONSchemaModel):
                value = cls(value,
                    set_defaults=self._set_defaults,
                    schemas_loader=getattr(self, "_$schemas_loader"))
            elif issubclass(cls, ObjectDict):
                value = cls(value,
                    schemas_loader=getattr(self, "_$schemas_loader"))
            else:
                value = cls(value)
            
            if prop_name and original_type != type(value):
                self._set_property(prop_name, value)
        return value
    
    def _validate(self):
        """Validate the value of this instance to match the schema."""
        validictory.validate(self, self._schema_data, required_by_default=False)
    
    @staticmethod
    def json_model_factory(name, schema, extends=None, **kwargs):
        """Return a class type of JSONSchemaModel based on schema."""
        
        if isinstance(extends, (list, tuple)):
            raise ValueError("Support only single inheritance")
        
        parent = extends or JSONSchemaModel
        parent_meta = getattr(parent, '__metaclass__', None)
        meta = schemaMetaFactory("%sMeta" % name, schema, extends=parent_meta)
        return meta(name, (parent, ), {'__metaclass__': meta})


class SchemasLoader(object):
    """JSON Schema Loader"""
    __CACHE__ = {}
    __CLASSES_CACHE__ = {}
    __LOCATIONS__ = {}
    
    def __init__(self, locations=None, cache=None, class_cache=None):
        assert isinstance(locations, (dict, type(None))), \
            "locations is not of type dict or None."
        assert isinstance(cache, (dict, type(None))), \
            "cache is not of type dict or None."
        assert isinstance(class_cache, (dict, type(None))), \
            "class_cache is not of type dict or None."
        self.__LOCATIONS__ = locations or {}
        self.__CACHE__ = cache or {}
        self.__CLASSES_CACHE__ = class_cache or {}
    
    def get(self, uri):
        if uri in self.__CACHE__:
            return self.__CACHE__[uri]
        location = self.__LOCATIONS__.get(uri, uri)
        return self._load_schema(location)
    
    def get_class(self, schema_uri, class_name=None, extends=None, *args, **kwargs):
        """Return a class type of JSONSchemaModel based on schema."""
        if schema_uri in self.__CLASSES_CACHE__:
            return self.__CLASSES_CACHE__[schema_uri]
        schema = self.get(schema_uri)
        class_name = class_name or str(schema.get("name", None))
        if not class_name:
            raise AttributeError(
                "class_name is defined and the schema has not 'name'.")
        cls = JSONSchemaModel.json_model_factory(class_name, schema, extends,
            *args, **kwargs)
        self.set_class(schema_uri, cls)
        return cls
    
    def set_class(self, schema_uri, cls):
        """Set a class type to returned by get_class."""
        self.__CLASSES_CACHE__[schema_uri] = cls
    
    def _load_schema(self, name):
         raise NotImplementedError("Schemas._load_schema is not implemented")


class SchemasHTTPLib2(SchemasLoader):
    """Relies on HTTPLib2 HTTP client to load schemas"""
    def __init__(self, http, locations=None, cache=None, class_cache=None):
        super(SchemasHTTPLib2, self).__init__(locations, cache, class_cache)
        self._http = http
     
    def _load_schema(self, uri):
        resp, content = self._http.request(uri, "GET")
        self.__CACHE__[uri] = json.loads(content)
        # Work around that 'extends' is not supported in validictory
        json_schema_merge_extends(self.__CACHE__[uri], self.__CACHE__)
        return self.__CACHE__[uri]


class SchemasAsyncHTTP(SchemasLoader):
    """Relies on Tornado's AsyncHTTP client to load schemas"""
    def __init__(self, async_http, locations=None, cache=None, class_cache=None):
        super(SchemasAsyncHTTP, self).__init__(locations, cache, class_cache)
        self._http = async_http
    
    def _save_schema(self, response, uri, callback):        
        self.__CACHE__[uri] = json.loads(response.body)
        # Work around that 'extends' is not supported in validictory
        json_schema_merge_extends(self.__CACHE__[uri], self.__CACHE__)
        callback(self.__CACHE__[uri])
    
    def get(self, uri, callback):
        if not callback:
            raise ValueError("callback is not defined.")
        if uri in self.__CACHE__:
            callback(self.__CACHE__[uri])
        else:
            location = self.__LOCATIONS__.get(uri, uri)
            self._load_schema(location, callback)
     
    def _load_schema(self, uri, callback):
        cb = functools.partial(callback, uri=uri)
        self._http.fetch(uri, callback=cb)


def json_object_hook(json_object, schemas, default_class=None):
    default_class = default_class or ObjectDict
    if "$schema" in json_object:
        cls = schemas.get_class(json_object["$schema"])
    return cls(json_object)
    
        

# Define the default JSON Schemas that are defiend in the JSON schema RFC
JSON_SCHEMA = json.loads(open(JSON_SCHEMAS_ROOT + "/schema").read())
HYPER_SCHEMA = json.loads(open(JSON_SCHEMAS_ROOT + "/hyper-schema").read())
JSON_REF_SCHEMA = json.loads(open(JSON_SCHEMAS_ROOT + "/json-ref").read())
HYPER_LINKS_SCHEMA = json.loads(open(JSON_SCHEMAS_ROOT + "/links").read())

CACHE = {
    "http://json-schema.org/draft-03/schema#": JSON_SCHEMA,
    "http://json-schema.org/draft-03/hyper-schema#": HYPER_SCHEMA,
    "http://json-schema.org/draft-03/links#": HYPER_LINKS_SCHEMA,
    "http://json-schema.org/draft-03/json-ref#": JSON_REF_SCHEMA,
}

http_client = httplib2.Http(".cache")
schemaLoader = SchemasHTTPLib2(http_client, cache=CACHE)

JSONSchema = schemaLoader.get_class(
    "http://json-schema.org/draft-03/schema#", "JSONSchema")
HyperSchema = schemaLoader.get_class(
    "http://json-schema.org/draft-03/hyper-schema#", "HyperSchema")
HyperLink = schemaLoader.get_class(
    "http://json-schema.org/draft-03/links#", "HyperLink")
JSONRef = schemaLoader.get_class(
    "http://json-schema.org/draft-03/json-ref#", "JSONRef")

# Load the basic Network Resources defined by UNIS
NetworkResourceMeta = schemaMetaFactory("NetworkResourceMeta",  schema=schemaLoader.get(SCHEMAS["networkresource"]))
MetadataMeta = schemaMetaFactory("MetadataMeta",  schema=schemaLoader.get(SCHEMAS["metadata"]))

class NetworkResource(JSONSchemaModel):
    __metaclass__ = NetworkResourceMeta
    def __init__(self, data=None, set_defaults=True, schemas_loader=None,
        auto_id=True, auto_ts=True):
        JSONSchemaModel.__init__(self, 
            data=data,
            set_defaults=set_defaults,
            schemas_loader=schemas_loader
        )
        if auto_id:
            self.id = self.id or str(ObjectId())
        if auto_ts:
            self.ts = self.ts or int(time.time() * 1000000)

class Metadata(JSONSchemaModel):
    __metaclass__ = MetadataMeta
    def __init__(self, data=None, set_defaults=True, schemas_loader=None,
        auto_id=True, auto_ts=True):
        JSONSchemaModel.__init__(self, 
            data=data,
            set_defaults=set_defaults,
            schemas_loader=schemas_loader
        )
        if auto_id:
            self.id = self.id or str(ObjectId())
        if auto_ts:
            self.ts = self.ts or int(time.time() * 1000000)

Node = schemaLoader.get_class(SCHEMAS["node"], extends=NetworkResource)
Link = schemaLoader.get_class(SCHEMAS["link"], extends=NetworkResource)
Port = schemaLoader.get_class(SCHEMAS["port"], extends=NetworkResource)
Path = schemaLoader.get_class(SCHEMAS["path"], extends=NetworkResource)
Service = schemaLoader.get_class(SCHEMAS["service"], extends=NetworkResource)
Network = schemaLoader.get_class(SCHEMAS["network"], extends=Node)
Domain = schemaLoader.get_class(SCHEMAS["domain"], extends=NetworkResource)
Topology = schemaLoader.get_class(SCHEMAS["topology"], extends=NetworkResource)
Event = schemaLoader.get_class(SCHEMAS["datum"], extends=NetworkResource)
Data = schemaLoader.get_class(SCHEMAS["data"], extends=NetworkResource)
