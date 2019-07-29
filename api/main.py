from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all
from aws_xray_sdk.core.models import http
import os
import logging

API_VERSION =  os.environ['API_VERSION']

patch_all()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# xray_recorder.configure(
#     sampling=False,
#     context_missing='LOG_ERROR',
#     plugins=('EC2Plugin', 'ECSPlugin'),
#     service='Flask Api %s'%(API_VERSION)
# )
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

class Ping(Resource):
    def get(self):
        return {'response': 'ok'}

class Todo(Resource):
    def __init__(self):
        parser.add_argument('x-traceid', location='headers')
        parser.add_argument('x-parentid', location='headers')
        rgs = parser.parse_args()
        self.traceid = rgs["x-traceid"]
        self.parentid = rgs["x-parentid"]
        segment = xray_recorder.begin_segment('api_%s_todo'%(API_VERSION),traceid = self.traceid, parent_id=self.parentid,sampling=1)
        segment.put_http_meta(http.URL, 'api-%s.flask.sample'%(API_VERSION))
        logger.info("get todo from api ver%s"%(API_VERSION))

    def __del__(self):
        xray_recorder.end_segment()

    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        logger.info("trace id %s"%self.traceid)
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
    def __init__(self):
        parser.add_argument('x-traceid', location='headers')
        parser.add_argument('x-parentid', location='headers')
        rgs = parser.parse_args()
        self.traceid = rgs["x-traceid"]
        self.parentid = rgs["x-parentid"]
        segment = xray_recorder.begin_segment('api_%s_todos'%(API_VERSION), traceid = self.traceid, parent_id=self.parentid,sampling=1)
        segment.put_http_meta(http.URL, 'api-%s.flask.sample'%(API_VERSION))
        logger.info("get todos from api ver%s"%(API_VERSION))

    def __del__(self):
        xray_recorder.end_segment()

    def get(self):
        logger.info("trace id %s"%self.traceid)
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
