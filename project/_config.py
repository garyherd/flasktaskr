import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
WTF_CSRF_ENABLED = True
SECRET_KEY = \
    r'\x9b\x9b\x1b\x9b<\xbc\xd6kES\x8b\xb3\xa9\xa6\xf6x)*\x04%\xf30\x1e\xef'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH

DEBUG = False

