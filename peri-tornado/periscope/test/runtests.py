#!/usr/bin/env python
import argparse
import os
import sys
import unittest
from tornado.options import define, options, parse_command_line

define("all", default=False, type=None, help="Run all tests.")
define("integration", default=False, type=None, help="Run integration tests.")
define("unit", default=True, type=None, help="Run unit tests.")

RUN_UNIT_TESTING = True
RUN_INTEGRATION_TESTING = False

UNIT_TEST_MODULES = [
    'periscope.test.db_test.DBLayerTest',
    'periscope.test.db_test.DBLayerTest',
    'periscope.test.models_test.ObjectDictTest',
    'periscope.test.models_test.SchemasLoaderTest',
    'periscope.test.models_test.JSONSchemaModelTest',
    'periscope.test.handlers_test.NetworkResourceHandlerTest',
    'periscope.test.handlers_test.SSEHandlerTest',
    'periscope.test.utils_test',
]

INTEGRATION_TEST_MODULES = [
    'periscope.test.db_test.DBLayerIntegrationTest',
    'periscope.test.handlers_test.NetworkResourceHandlerIntegrationTest',
    'periscope.test.handlers_test.CollectionHandlerIntegrationTest',
]


def all():
    #Setting up path names
    PERISCOPE_ROOT = os.path.dirname(os.path.abspath(__file__)) + os.sep
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(PERISCOPE_ROOT))))
    test_modules = []
    
    if RUN_UNIT_TESTING:
        test_modules.extend(UNIT_TEST_MODULES)
    if RUN_INTEGRATION_TESTING:
        test_modules.extend(INTEGRATION_TEST_MODULES)
    
    return unittest.defaultTestLoader.loadTestsFromNames(test_modules)

if __name__ == '__main__':
    import tornado.testing
    parse_command_line()
    
    RUN_UNIT_TESTING = options.unit
    RUN_INTEGRATION_TESTING = options.integration
    
    if options.all:
        RUN_UNIT_TESTING = True
        RUN_INTEGRATION_TESTING = True
    
    tornado.testing.main()
