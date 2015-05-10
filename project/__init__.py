# project/__init__.py


from flask import Flask, render_template, request, make_response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Api
import datetime

app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
_api_v2 = Api(app)

from project.users.views import users_blueprint
from project.tasks.views import task_blueprint
from project.api.views import api_blueprint
from project.api_v2.views import api_v2_blueprint

# register our blueprint
app.register_blueprint(users_blueprint)
app.register_blueprint(task_blueprint)
app.register_blueprint(api_blueprint)
app.register_blueprint(api_v2_blueprint)

def write_to_error_log(url, error):
    now = datetime.datetime.now()
    r = url
    with open('error.log', 'a') as f:
        current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
        f.write("\n{} error at {}: {}".format(error, current_timestamp, r))


@app.errorhandler(404)
def not_found(error):
    if app.debug is not True:
        write_to_error_log(request.url, error)

    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if app.debug is not True:
        write_to_error_log(request.url, error)

    return render_template('500.html'), 500


@app.errorhandler(405)
def method_not_allowed_error(error):
    if app.debug is not True:
        write_to_error_log(request.url, error)

    result = {'status': 'error',
              'error description': 'GET request not allowed here'}
    code = 405
    return make_response(jsonify(result), code)

@app.errorhandler(401)
def unauthorized_error(error):
    if app.debug is not True:
        write_to_error_log(request.url, error)

    result = {'status': 'error',
              'error description': 'user name or password invalid'}
    code = 405
    return make_response(jsonify(result), code)



