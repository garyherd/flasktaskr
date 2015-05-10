# tests/test_api_v2.py


import os
import base64
import unittest
from datetime import date
import json


from project import app, db, bcrypt
from project._config import basedir
from project.models import Task


TEST_DB = 'test.db'


class APIv2Tests(unittest.TestCase):

    ##########################
    #### setup and teardown ##
    ##########################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    ###############################
    #### helper methods ###########
    ###############################

    def add_tasks(self):
        db.session.add(
            Task(
                "Run around in circles",
                date(2015, 10, 22),
                10,
                date(2015, 10, 5),
                1,
                1
            )
        )
        db.session.commit()

        db.session.add(
            Task(
                "Purchase Real Python",
                date(2016, 2, 23),
                10,
                date(2015, 2, 7),
                1,
                1
            )
        )
        db.session.commit()

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password,
                      confirm=confirm),
            follow_redirects=True)

    ################
    #### tests #####
    ################

    def test_collection_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v2/tasks/', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Run around in circles', response.data)
        self.assertIn(b'Purchase Real Python', response.data)


    def test_resource_endpoint_returns_correct_data(self):
        self.add_tasks()
        response = self.app.get('api/v2/tasks/2', follow_redirects=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Purchase Real Python', response.data)
        self.assertNotIn(b'Run around in circles', response.data)


    def test_invalid_resource_endpoint_returns_error(self):
        self.add_tasks()
        response = self.app.get('api/v2/tasks/209', follow_redirects=True)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Element does not exist', response.data)


    def test_valid_user_can_insert_a_task(self):
        self.register('Michael', 'michael@realpython.com', 'python2015',
              'python2015')
        encoded = base64.standard_b64encode('Michael:python2015')
        header = {'authorization': 'Basic {}'.format(encoded),
                  'Content-Type': 'application/json'}
        data = {'name': "test api task", 'due_date': '05/25/2018',
                'priority': 6}
        # data = dict(name="test api task", due_date='05/25/2018',
        #         priority= 6)
        response = self.app.post('api/v2/tasks/', headers=header,
                                 data=json.dumps(data))
        # response = requests.post(url='api/v2/tasks/',
        #                          auth=HTTPBasicAuth('Michael', 'python2015'),
        #                          data=data)
        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.mimetype, 'application/json')
        self.assertIn(b'Entry was successfully posted', response.data)
