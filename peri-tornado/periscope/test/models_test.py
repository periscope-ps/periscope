#!/usr/bin/env python
"""
Models related tests
"""

import copy
from mock import MagicMock
from periscope.models import ObjectDict
from periscope.models import JSONSchemaModel
from periscope.models import SchemasLoader
from periscope.test.base import PeriscopeTestCase


class ObjectDictTest(PeriscopeTestCase):
    def test_init(self):
        # Arrange
        test_data = {"key1": "value1", "key2": "value2", "$key3": "value3"}
        # Act
        obj1 = ObjectDict()
        obj2 = ObjectDict(test_data)
        # Assert
        self.assertEqual(obj1, {})
        self.assertEqual(obj2, test_data)
        for key, value in test_data.items():
            self.assertTrue(hasattr(obj2, key))
            self.assertEqual(getattr(obj2, key), value)
        
    def test_add_property(self):
        # Arrange
        test_data = {"key1": "value1", "key2": "value2", "$key3": "value3"}
        obj = ObjectDict(test_data)
        # Act
        obj.key4 = "value4"
        obj["key5"] = "value5"
        # Assert
        self.assertTrue(hasattr(obj, "key4"))
        self.assertEqual(getattr(obj, "key4"), "value4")
        self.assertTrue(hasattr(obj, "key5"))
        self.assertEqual(getattr(obj, "key5"), "value5")
        self.assertNotEqual(obj, test_data)
        for key, value in test_data.items():
            self.assertTrue(hasattr(obj, key))
            self.assertEqual(getattr(obj, key), value)
    
    def test_del_property(self):
        # Arrange
        test_data = {"key1": "value1", "key2": "value2", "$key3": "value3"}
        obj = ObjectDict(test_data)
        # Act
        del obj.key1
        del obj["key2"]
        # Assert
        self.assertNotEqual(obj, test_data)
        self.assertFalse(hasattr(obj, "key1"))
        self.assertFalse(hasattr(obj, "key2"))
        self.assertFalse("key1" in obj)
        self.assertFalse("key2" in obj)
        self.assertTrue(hasattr(obj, "$key3"))
        self.assertEqual(getattr(obj, "$key3"), "value3")
    
    def test_convert_value(self):
        # Arrange
        test_data = {"key1": "value1",
            "key2": {"k1": "v1"},
            "key3": {"k2": {"k3": "v3"}}}
        obj = ObjectDict(test_data)
        # Act
        key1 = obj.key1
        key2 = obj["key2"]
        key3 = obj.key3
        k1 = key2.k1
        k2 = key3["k2"]
        k3 = k2.k3
        # Assert
        self.assertEqual(obj, test_data)
        self.assertTrue(isinstance(obj, ObjectDict))
        self.assertTrue(isinstance(key1, str))
        self.assertTrue(isinstance(key2, ObjectDict))
        self.assertTrue(isinstance(key3, ObjectDict))
        self.assertTrue(isinstance(k1, str))
        self.assertTrue(isinstance(k2, ObjectDict))
        self.assertTrue(isinstance(k3, str))
        
    def test_convert_value_nested(self):
        # Arrange
        test_data = {"key1": "value1",
            "key2": {"k1": "v1"},
            "key3": {"k2": {"k3": "v3"}},
            "key4": [{"k4": {"k5": "v5"}}]
        }
        expected_data = {"key1": "value1",
            "key2": {"k1": "v1"},
            "key3": {"k2": {"k3": "v3"}},
            "key4": [{"k4": {"k5": "v5"}}, {"k6": "v6"}],
            "key5": {"k7": [{"k8": "v8"}, {"k9": "v9"}]}
        }
        obj = ObjectDict(test_data)
        # Act
        
        key1 = obj.key1
        key2 = obj["key2"]
        key3 = obj.key3
        key4 = obj.key4
        k1 = key2.k1
        k2 = key3["k2"]
        k3 = k2.k3
        key4 = obj.key4
        key4.append({"k6": "v6"})
        obj.key5 = {"k7": [{"k8": "v8"}]}
        k7 = obj.key5.k7
        k7.append({"k9": "v9"})
        # Assert
        self.assertEqual(obj, expected_data)
        self.assertTrue(isinstance(obj, ObjectDict))
        self.assertTrue(isinstance(key1, str))
        self.assertTrue(isinstance(key2, ObjectDict))
        self.assertTrue(isinstance(key3, ObjectDict))
        self.assertTrue(isinstance(k1, str))
        self.assertTrue(isinstance(k2, ObjectDict))
        self.assertTrue(isinstance(k3, str))

        
    def test_to_mongo(self):
        # Arrange
        obj = ObjectDict()
        obj["$prop1"] = "value1"
        obj["prop.2"] = "value2"
        obj["prop.$3"] = "value3"
        obj["prop4"] = copy.deepcopy(obj)
        obj["prop5"] = [{"key.1": "v1", "$key2": "v2"}]
        expected = {
            "\$prop1": "value1",
            "prop$DOT$2": "value2", 
            "prop$DOT$$3": "value3", 
            "prop4": {
                "\$prop1": "value1",
                "prop$DOT$2": "value2", 
                "prop$DOT$$3": "value3", 
            },
            "prop5": [
                {
                    "key$DOT$1": "v1",
                    "\$key2": "v2"
                }
            ]
        }

        # Act
        mongo_dict = dict(obj._to_mongoiter())
        # Assert
        self.assertTrue(hasattr(obj, "$prop1"))
        self.assertTrue(hasattr(obj, "prop.2"))
        self.assertTrue(hasattr(obj, "prop.$3"))
        self.assertEqual(obj["$prop1"], "value1")
        self.assertEqual(obj["prop.2"], "value2")
        self.assertEqual(obj["prop.$3"], "value3")
        self.assertEqual(mongo_dict, expected)
        
    def test_from_mongo(self):
        # Arrange
        data = {
            "\$prop1": "value1",
            "prop$DOT$2": "value2", 
            "prop$DOT$$3": "value3", 
            "prop4": {
                "\$prop1": "value1",
                "prop$DOT$2": "value2", 
                "prop$DOT$$3": "value3", 
            },
            "prop5": [
                {
                    "key$DOT$1": "v1",
                    "\$key2": "v2"
                }
            ]
        }
        
        # Act
        obj = ObjectDict._from_mongo(data)
        # Assert
        self.assertTrue(isinstance(obj, ObjectDict))
        self.assertTrue(hasattr(obj, "$prop1"))
        self.assertTrue(hasattr(obj, "prop.2"))
        self.assertTrue(hasattr(obj, "prop.$3"))
        self.assertTrue(hasattr(obj, "prop4"))
        self.assertTrue(hasattr(obj, "prop5"))
        self.assertEqual(obj["$prop1"], "value1")
        self.assertEqual(obj["prop.2"], "value2")
        self.assertEqual(obj["prop.$3"], "value3")
        self.assertEqual(obj["prop4"],  \
            {"$prop1": "value1", "prop.2": "value2", "prop.$3": "value3"})
        self.assertEqual(obj["prop5"], [{"key.1": "v1", "$key2": "v2"}])


class JSONSchemaModelTest(PeriscopeTestCase):
    def test_init(self):
        # Arrange
        schema = {"name": "TestSchema",
            "description": "Unit testing schema",
            "additionalProperties": False,
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "prop1 description",
                },
                "prop2": {
                    "type": "integer",
                    "description": "prop2 description",
                },
            },
            "patternPropeties": {
                "prop?": {
                    "type": "string",
                    "description": "pattern prop",
                },
            },
        }
        # Act
        schemaModel = JSONSchemaModel.json_model_factory("schemaModel", schema)
        # Assert
        self.assertTrue(issubclass(schemaModel, JSONSchemaModel))
        self.assertEqual(schemaModel.__doc__, schema["description"])
        self.assertTrue(hasattr(schemaModel, "prop1"))
        self.assertTrue(hasattr(schemaModel, "prop2"))
        
    def test_set_value(self):
        # Arrange
        schema = {"name": "TestSchema",
            "description": "Unit testing schema",
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "prop1 description",
                },
                "prop2": {
                    "type": "string",
                    "description": "prop2 description",
                },
            },
            "patternProperties": {
                "prop?": {
                    "type": "string",
                    "description": "pattern prop",
                },
            },
        }
        SchemaModel = JSONSchemaModel.json_model_factory("schemaModel", schema)
        schemaModel = SchemaModel()
        # Act
        schemaModel.prop1 = "value1"
        schemaModel["prop2"] = "value2"
        schemaModel.prop3 = "value3"
        schemaModel["prop4"] = "value4"
        # Assert
        self.assertTrue(hasattr(schemaModel, "prop1"))
        self.assertTrue(hasattr(schemaModel, "prop2"))
        self.assertTrue(hasattr(schemaModel, "prop3"))
        self.assertTrue(hasattr(schemaModel, "prop4"))
        self.assertEqual(schemaModel.prop1, "value1")
        self.assertEqual(schemaModel.prop2, "value2")
        self.assertEqual(schemaModel.prop3, "value3")
        self.assertEqual(schemaModel.prop4, "value4")
        self.assertEqual(schemaModel["prop1"], "value1")
        self.assertEqual(schemaModel["prop2"], "value2")
        self.assertEqual(schemaModel["prop3"], "value3")
        self.assertEqual(schemaModel["prop4"], "value4")
        
    
    def test_json_model_factory(self):
        # Arrange
        schema = {"name": "TestSchema",
            "description": "Unit testing schema",
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "prop1 description",
                },
                "prop2": {
                    "type": "string",
                    "description": "prop2 description",
                },
            },
            "patternProperties": {
                "prop?": {
                    "type": "string",
                    "description": "pattern prop",
                },
            },
        }
        schema2 = {"name": "TestSchema2",
            "description": "Unit testing schema2",
            "properties": {
                "p1": {
                    "type": "string",
                    "description": "prop1 description",
                }
            }
        }
        
        # Act
        Schema = JSONSchemaModel.json_model_factory("Schema", schema)
        Schema2 = JSONSchemaModel.json_model_factory("Schema2", schema2,
            extends=Schema)
        schemaModel = Schema()
        schemaModel.prop1 = "value1"
        schemaModel["prop2"] = "value2"
        schemaModel.prop3 = "value3"
        schemaModel["prop4"] = "value4"
        schemaModel2 = Schema2()
        # Assert
        self.assertTrue(hasattr(schemaModel, "prop1"))
        self.assertTrue(hasattr(schemaModel, "prop2"))
        self.assertTrue(hasattr(schemaModel, "prop3"))
        self.assertTrue(hasattr(schemaModel, "prop4"))
        self.assertEqual(schemaModel.prop1, "value1")
        self.assertEqual(schemaModel.prop2, "value2")
        self.assertEqual(schemaModel.prop3, "value3")
        self.assertEqual(schemaModel.prop4, "value4")
        self.assertEqual(schemaModel["prop1"], "value1")
        self.assertEqual(schemaModel["prop2"], "value2")
        self.assertEqual(schemaModel["prop3"], "value3")
        self.assertEqual(schemaModel["prop4"], "value4")
    
    def test_nested_schemas(self):
        # Arrange
        schema = {"name": "TestSchema",
            "description": "Unit testing schema",
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "prop1 description",
                },
                "prop2": {
                    "type": [{"$ref": "schema2"}],
                    "description": "prop2 description",
                },
            }
        }
        schema2 = {"name": "TestSchema2",
            "description": "Unit testing schema2",
            "properties": {
                "p1": {
                    "type": "string",
                    "description": "prop1 description",
                }
            }
        }
        data = {
            "prop1": "value1",
            "prop2": {
                "p1": "value2",
            }
        }
        Schema = JSONSchemaModel.json_model_factory("Schema", schema)
        Schema2 = JSONSchemaModel.json_model_factory("Schema2", schema2,
            extends=Schema)
        loader_mock = SchemasLoader()
        loader_mock.get_class = MagicMock()
        loader_mock.get_class.return_value = Schema2
        
        # Act
        schemaModel = Schema(data, schemas_loader=loader_mock)
        # Assert
        self.assertTrue(hasattr(schemaModel, "prop1"))
        self.assertTrue(hasattr(schemaModel, "prop2"))
        self.assertEqual(schemaModel.prop1, data["prop1"])
        self.assertEqual(schemaModel.prop2, data["prop2"])
        self.assertEqual(schemaModel["prop1"], data["prop1"])
        self.assertEqual(schemaModel["prop2"], data["prop2"])
        self.assertEqual(type(schemaModel.prop2), Schema2)



class SchemasLoaderTest(PeriscopeTestCase):
    def test_init(self):
        # Arrange
        schema = {
            "id": "http://schema1",
            "name": "TestSchema",
            "description": "Unit testing schema",
            "properties": {
                "prop1": {
                    "type": "string",
                    "description": "prop1 description",
                },
                "prop2": {
                    "type": "string",
                    "description": "prop2 description",
                },
            },
            "patternProperties": {
                "prop?": {
                    "type": "string",
                    "description": "pattern prop",
                },
            },
        }
        cache = {schema["id"]: schema}
        # Act
        obj = SchemasLoader(cache=cache)
        schema_get = obj.get(schema["id"])
        # Assert
        self.assertTrue(isinstance(obj, SchemasLoader))
        self.assertEqual(schema_get, schema)

