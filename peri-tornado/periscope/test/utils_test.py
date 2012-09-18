
import copy
import json
from mock import patch
from StringIO import StringIO
import urllib2
import validictory

from periscope.test.base import PeriscopeTestCase
import periscope.utils as utils

class UtilsTest(PeriscopeTestCase):
    @patch.object(urllib2, 'urlopen', mocksignature=False)
    def test_load_json_url(self, url_open_mock):
        # Arrange
        res1_url = "http://somenotdefinedsite/res1"
        res2_url = "http://somenotdefinedsite/res2"
        res3_url = "http://somenotdefinedsite/res3"
        res1 = {"id": "res1"}
        res2 = {"id": "res2"}
        res3 = {"id": "res3"}
        res2_id = res2["id"]
        cached_urls = {
            res1_url: res1,
            res2_url: res2,
        }
        all_urls = {
            res1_url: res1,
            res2_url: res2,
            res3_url: res3,
        }
        url_open_mock.side_effect = lambda url, *args, **kwargs: StringIO(json.dumps(all_urls[url]))
        
        # Act
        loaded_res1 = utils.load_json_url(res1_url, cache=cached_urls)
        loaded_res2 = utils.load_json_url(res2_url, cache=cached_urls)
        loaded_res2["id"] = "new id"
        loaded_res3 = utils.load_json_url(res3_url, cache=cached_urls)
        
        # Assert
        self.assertEqual(loaded_res1, res1)
        self.assertNotEqual(loaded_res2, res2)
        self.assertEqual(loaded_res3, res3)


    @patch.object(utils, 'load_json_url', mocksignature=False)
    def test_load_json_refs(self, load_json_url_mock):
        # Arrange
        res1 = {"id": "loaded URL"}
        load_json_url_mock.return_value = res1
        
        ref_direct = {"id": 1, "ref_value": {"$ref": "http://example.com/"}}
        ref_in_array = {"id": 1, "ref_array": ["someelement", {"$ref": "http://example.com/"}]}
        ref_deep = {"id": 1, "ref_parent": {"ref_value": {"$ref": "http://example.com/"}}}
        ref_deep_array = {"id": 1, "ref_parent": ["someelement", {"ref_value": {"$ref": "http://example.com/"}}]}
        ref_deep_array2 = {"id": 1, "ref_parent": ["someelement", {"$ref": "http://example.com/"}]}
        # Act
        utils.load_json_refs(ref_direct)
        utils.load_json_refs(ref_in_array)
        utils.load_json_refs(ref_deep)
        utils.load_json_refs(ref_deep_array)
        utils.load_json_refs(ref_deep_array2)
        # Assert
        self.assertEqual(ref_direct["ref_value"], res1)
        self.assertEqual(ref_in_array["ref_array"][1], res1)
        self.assertEqual(ref_deep["ref_parent"]["ref_value"], res1)
        self.assertEqual(ref_deep_array["ref_parent"][1]["ref_value"], res1)
        self.assertEqual(ref_deep_array2["ref_parent"][1], res1)
        
    
    def test_json_schema_merge_extends(self):
        # Arraneg
        parent_schema = {"id": "parentschema",
            "additionalProperties": False,
            "properties": {"parent_prop": {"type": "string"}}
        }
        child_schema = {"id": "childschema",
            "additionalProperties": False,
            "extends": parent_schema,
            "properties": {"child_prop": {"type": "string"}}
        }
        child2_schema = {"id": "childschema",
            "additionalProperties": False,
            "extends": child_schema,
            "properties": {"child_prop2": {"type": "string"}}
        }
        child3_schema = {"id": "childschema",
            "additionalProperties": False,
            "extends": child_schema,
            "properties": {
                "child_prop3": {"type": "string"},
                "child_extend": {
                    "extends": parent_schema,
                    "properties": {
                        "sub_child":{
                            "type": "string"
                        }
                    }
                }
            }
        }
        
        parent_schema_copy = copy.copy(parent_schema)
        child_schema_copy = copy.copy(child_schema)
        child2_schema_copy = copy.copy(child2_schema)
        child3_schema_copy = copy.copy(child3_schema)
        
        # Act
        utils.json_schema_merge_extends(parent_schema_copy)
        utils.json_schema_merge_extends(child_schema_copy)
        utils.json_schema_merge_extends(child2_schema_copy)
        utils.json_schema_merge_extends(child3_schema_copy)
        
        # Assert
        self.assertEqual(child_schema_copy["properties"].get("parent_prop", None), 
                        parent_schema["properties"]["parent_prop"])
        self.assertEqual(child2_schema_copy["properties"].get("parent_prop", None), 
                        parent_schema["properties"]["parent_prop"])
        self.assertEqual(child2_schema_copy["properties"].get("parent_prop", None), 
                        child_schema["properties"]["child_prop"])
        self.assertEqual(child3_schema_copy["properties"].get("parent_prop", None), 
                        parent_schema["properties"]["parent_prop"])
        self.assertEqual(child3_schema_copy["properties"].get("parent_prop", None), 
                        child_schema["properties"]["child_prop"])
        self.assertEqual(child3_schema_copy["properties"]["child_extend"]["properties"].get("parent_prop", None), 
                        parent_schema["properties"]["parent_prop"])

    @patch.object(utils, 'load_json_url', mocksignature=False)    
    def test_validate_json(self, load_json_url_mock):
        # Arrange
        parent_schema = {"id": "parentschema",
            "additionalProperties": False,
            "properties": {"parent_prop": {"type": "string"}}
        }
        child_schema = {"id": "childschema",
            "additionalProperties": False,
            "extends": {"$ref": "parentschema"},
            "properties": {"child_prop": {"type": "string"}}
        }
        doc = {"parent_prop": "parent_prop test", "child_prop": "child_prop test"}
        load_json_url_mock.return_value = parent_schema
        # Act
        utils.validate_json(doc, child_schema)
        
