# project/api/views.py


from functools import wraps
from flask import flash, redirect, jsonify, \
    session, url_for, Blueprint, make_response, request
from flask_restful import reqparse

from project import db
from project.models import Task


################
#### config ####
################

api_blueprint = Blueprint('api', __name__)

##########################
#### helper functions ####
##########################


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first')
            return redirect(url_for('users.login'))
    return wrap


def open_tasks():
    return db.session.query(Task).filter_by(
        status='1').order_by(Task.due_date.asc())


def closed_tasks():
    return db.session.query(Task).filter_by(
        status='0').order_by(Task.due_date.asc())

parser = reqparse.RequestParser()
parser.add_argument('task', type=str)


################
#### routes ####
################

@api_blueprint.route('/api/v1/tasks/')
def api_tasks():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_results = []
    for result in results:
        data = {
            'task_id': result.task_id,
            'task_name': result.name,
            'due_date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user id': result.user_id
        }
        json_results.append(data)
    return jsonify(items=json_results)

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def task(task_id):
    result = db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        result = {
            'task_id': result.task_id,
            'task_name': result.name,
            'due_date': str(result.due_date),
            'priority': result.priority,
            'posted date': str(result.posted_date),
            'status': result.status,
            'user id': result.user_id
        }
        code = 200
    else:
        result = {"error": "Element does not exist"}
        code = 404
    return make_response(jsonify(result), code)

@api_blueprint.route('/api/v1/add_task', methods=['POST'])
def  api_add_task():
    error = None
    # TODO: maybe wrap this in a try/catch block
    if request.method == 'POST':

        args = parser.parse_args()
        result = {"status": "POST was received", "task_to_add": args['task']}
        code = 201
    else:
        result = {"status": "GET request not allowed here"}
        code = 405
    return make_response(jsonify(result), code)



