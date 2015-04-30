import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'





class UserTest(unittest.TestCase):

    # helper methods
    def login(self, name, password):
        return self.app.post('/', data=dict(
            name=name, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password,
                      confirm=confirm),
            follow_redirects=True)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='02/05/2014',
            priority='1',
            posted_date='02/04/2014',
            status='1'
        ), follow_redirects=True)

    #######################
    # setup and teardown ##
    #######################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    # executed after to each test
    def tearDown(self):
        db.drop_all()

    # each test should start with 'test'
    def test_users_can_register(self):
        new_user = User("michael", "michael@mherman.org", "michaelherman")
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'michael'

    def test_form_is_present_on_login_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please sign in to access your task list',
                      response.data)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_users_can_login(self):
        self.register('Michael', 'michael@realpython.com', 'python',
                      'python')
        response = self.login('Michael', 'python')
        self.assertIn('Logout', response.data)

    # TODO: refactor for DRY?
    def test_invalid_form_data(self):
        self.register('Michael', 'm@realpython.com', 'python', 'python')
        response = self.login('alert("alert box!");', 'foo')
        self.assertIn(b'Invalid username or password.', response.data)

    # TODO: refactor to test form is preset?
    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.',
                      response.data)

    # TODO: refactor for DRY?
    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    # TODO: redfactor for DRY?
    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register(
            'Michael', 'michael@realpython.com', 'python', 'python')
        self.app.get('register/', follow_redirects=True)
        response = self.register(
            'Michael', 'michael@realpython.com', 'python', 'python')
        self.assertIn(
            b'That username and/or email already exist.', response.data
        )

    def test_logged_in_users_can_logout(self):
        self.register('Fletcher', 'fletcher@realpython.com', 'python101',
                      'python101')
        self.login('Fletcher', 'python101')
        response = self.logout()
        self.assertIn(b'Goodbye', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)

    def test_default_user_role(self):

        db.session.add(
            User(
                "Johnny",
                "john@doe.com",
                "johnny"
            )
        )

        db.session.commit()

        users = db.session.query(User).all()
        print users
        for user in users:
            self.assertEquals(user.role, 'user')


if __name__ == "__main__":
    unittest.main()

