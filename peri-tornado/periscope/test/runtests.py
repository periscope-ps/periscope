#!/usr/bin/env python

import os
import sys
import unittest


TEST_MODULES = [
    'periscope.test.models_test',
    'periscope.test.handlers_test',
]

def all():
    #Setting up path names
    PERISCOPE_ROOT = os.path.dirname(os.path.abspath(__file__)) + os.sep
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(PERISCOPE_ROOT))))

    return unittest.defaultTestLoader.loadTestsFromNames(TEST_MODULES)

if __name__ == '__main__':
    import tornado.testing
    #import periscope.app
    #periscope.app.conifg_logger
    tornado.testing.main()
