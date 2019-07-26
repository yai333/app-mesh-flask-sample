from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
import os

API_VERSION =  os.environ['API_VERSION']

xray_recorder.configure(
    sampling=False,
    context_missing='LOG_ERROR',
    plugins=('EC2Plugin', 'ECSPlugin'),
    service='Flask Api %s'%(API_VERSION)
)
app = Flask(__name__)
api = Api(app)
XRayMiddleware(app, xray_recorder)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

class Ping(Resource):
    def get(self):
        return {'response': 'ok'}

class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return {"todo":TODOS[todo_id], "version":API_VERSION}

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return {"response": "ok", "version":API_VERSION}, 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return {"todo":task, "version":API_VERSION}, 201

class TodoList(Resource):
    def get(self):
        return {"todos":TODOS, "version":API_VERSION}

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return {"todo":TODOS[todo_id], "version":API_VERSION}, 201


api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Ping, '/ping')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
