# project/api_v2/views.py


from functools import wraps
from flask import flash, redirect, session, url_for, Blueprint, g
from flask_restful import reqparse, Resource
from flask_httpauth import HTTPBasicAuth

from project import db, api__v2, bcrypt
from project.models import Task, User

from datetime import datetime


################
#  config   ####
################

api_v2_blueprint = Blueprint('api_v2', __name__)

auth = HTTPBasicAuth()

##########################
#   helper functions ####
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


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(name=username).first()
    if user is not None and bcrypt.check_password_hash(
            user.password, password):
        g.user = user
        return True
    else:
        return False


###################
#   Resources     #
###################

class ApiTaskList(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('name', type=str, location='json')
        self.post_parser.add_argument('due_date', type=str, location='json')
        self.post_parser.add_argument('priority', type=int, location='json')

    def get(self):
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
        return json_results

    @auth.login_required
    def post(self):
        args = self.post_parser.parse_args()
        new_task = Task(
            name=args['name'],
            due_date=datetime.strptime(args['due_date'], '%m/%d/%Y').date(),
            priority=args['priority'],
            posted_date=datetime.utcnow(),
            status='1',
            user_id=g.user.id
        )
        db.session.add(new_task)
        db.session.commit()
        result = {"status": "Entry was successfully posted",
                  "task added": args['name']}
        code = 201
        return result, code


class ApiTask(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('name', type=str, location='json')
        self.post_parser.add_argument('due_date', type=str, location='json')
        self.post_parser.add_argument('priority', type=int, location='json')

    def get(self, task_id):
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
        return result, code

    @auth.login_required
    def put(self, task_id):
        new_id = task_id
        task = db.session.query(Task).filter_by(task_id=new_id)
        if task:
            args = self.post_parser.parse_args()
            updated_task = {
                'name': args['name'],
                'due_date': datetime.strptime(
                    args['due_date'], '%m/%d/%Y').date(),
                'priority': args['priority'],
                'posted_date': datetime.utcnow(),
            }
            task.update(updated_task)
            db.session.commit()
            code = 201
            result = {"status": "task updated successfully"}
        else:
            result = {"error": "Element does not exist"}
            code = 404

        return result, code

    @auth.login_required
    def delete(self, task_id):
        new_id = task_id
        task = db.session.query(Task).filter_by(task_id=new_id)
        if task:
            task.delete()
            db.session.commit()
            code = 201
            result = {"status": "task deleted"}
        else:
            result = {"error": "Element does not exist"}
            code = 404

        return result, code


################
# routes       #
################

api__v2.add_resource(ApiTaskList, '/api/v2/tasks/')
api__v2.add_resource(ApiTask, '/api/v2/tasks/<int:task_id>')
