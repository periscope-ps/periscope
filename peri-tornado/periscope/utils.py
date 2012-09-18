import copy
import json
import urllib2
import validictory
import sys

def load_json_url(url, cache=None):
    """
    Loads a URL, if the url is already in cache it will load the cached 
    value. 
    """
    if not cache:
        cache = {}
    if url not in cache:
        doc = urllib2.urlopen(url)
        cache[url] = json.load(doc)
    res = cache.get(url)
    # Make sure to return a copy of the cache resource
    return copy.copy(res)


def load_json_refs(doc, cache=None):
    """
    Recursivly goes over json doc and load all $refs.
    NOTE: this function will change the actuall JSON document.
    """
    if isinstance(doc, list):
        for index in range(len(doc)):
            if isinstance(doc[index], dict):
                if "$ref" in doc[index]:
                    doc[index] = load_json_url(doc[index]["$ref"], cache)
                else:
                    load_json_refs(doc[index], cache)
    else:
        for key in doc:
            if isinstance(doc[key], dict):
                if "$ref" in doc[key]:
                    doc[key] = load_json_url(doc[key]["$ref"], cache)
                else:
                    load_json_refs(doc[key], cache)
            elif isinstance(doc[key], list):
                load_json_refs(doc[key], cache)


        
def json_schema_merge_extends(schema, cache=None):
    """
    Recursivly goes over json schema and merge all extends in the same schema.
    NOTE: this function will change the actuall JSON document.
    
    This is a work around to handle one level of schema extension!
    TODO (AH): find away to handle extends in a better way
    """
    if "extends" in schema:
        if "$ref" in schema["extends"]:
            load_json_refs(schema, cache)
        for prop in schema.get("extends", {}).get("properties", {}):
            if "properties" not in schema:
                continue
            if prop not in schema["properties"]:
                schema["properties"][prop] = schema["extends"]["properties"][prop]
    for key in schema:
        if isinstance(schema[key], dict):
            json_schema_merge_extends(schema[key], cache)
        elif isinstance(schema[key], list):
            for index in range(len(schema[key])):
                if isinstance(schema[key][index], dict):
                    if isinstance(schema[key], dict):
                        json_schema_merge_extends(schema[key], cache)
    schema.pop("extends", None)


def validate_json(doc, schema, cache=None):
    """
    Validates JSON doc based on the schema provided.
    
    NOTE: this function will change the actuall JSON document.
    NOTE: this function will change the actuall JSON schema.
    """
    # Copy json docs because load_json_refs is not safe
    docc = copy.copy(doc)
    schemac = copy.copy(schema)
    load_json_refs(docc, cache)
    load_json_refs(schemac, cache)
    json_schema_merge_extends(schemac, cache)
    return validictory.validate(docc, schemac)



def load_class(module_and_name):
    """Loads the module and returns the class."""    
    module, name = module_and_name.rsplit('.', 1)
    __import__(module)
    return getattr(sys.modules[module], name)


def class_fullname(obj):
    """Returns the full class name of an object"""
    return obj.__module__ + "." + obj.__class__.__name__
    
