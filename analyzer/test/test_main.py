from paste.fixture import TestApp
from nose.tools import *
from analyzer import main
import web

class TestCode():
    def get_app(self, middleware=[ ], db=False):
        if db:
            main.init_db(True)
        test_app = TestApp(main.app.wsgifunc(*middleware))
        return test_app

    def test_index(self):
        """Get home page
        """
        r = self.get_app().get('/')
        r.mustcontain('workflows')

    def test_list(self):
        """List top-level databases.
        """
        r = self.get_app(db=True).get('/wf/list')
        r.mustcontain('id')

    def test_specific(self):
        """Query a specific workflow UUID.
        """
        sample_uuid = 'FB005EAF-0FB8-4887-AA15-627DC61AC6E3'
        for type_ in 'info', 'xfrm', 'task':
            r = self.get_app().get('/wf/something/{0}'.format(type_), status=500)
            r = self.get_app().get('/wf/{1}/{0}'.format(type_, sample_uuid))
