from flask import Flask
from flask_restful import Resource, Api, reqparse
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
import requests
import os
import json


API_ENDPOINT =  os.environ['API_ENDPOINT']
SERVER_PORT =  os.environ['SERVER_PORT']
xray_recorder.configure(
    sampling=False,
    context_missing='LOG_ERROR',
    plugins=('EC2Plugin', 'ECSPlugin'),
    service='Flask Gateway'
)
app = Flask(__name__)
api = Api(app)
XRayMiddleware(app, xray_recorder)


parser = reqparse.RequestParser()
parser.add_argument('task')

class Ping(Resource):
    def get(self):
        return {'response': 'ok'}

class TodoList(Resource):
    def get(self):
        r = requests.get(url = '%s:%s/todos'%(API_ENDPOINT,SERVER_PORT))
        return r.json()

    def post(self):
        args = parser.parse_args()
        r = requests.post(url = '%s:%s/todos'%(API_ENDPOINT,SERVER_PORT), json=args)
        return r.json(), 201

class Todo(Resource):
    def get(self, todo_id):
        r = requests.get(url = '%s:%s/todos/%s'%(API_ENDPOINT,SERVER_PORT,todo_id))
        return r.json()

    def delete(self, todo_id):
        r = requests.delete(url = '%s:%s/todos/%s'%(API_ENDPOINT,SERVER_PORT,todo_id))
        return r.json(), 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        r = requests.put(url = '%s:%s/todos/%s'%(API_ENDPOINT,SERVER_PORT,todo_id), json=task)
        return r.json(), 201

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
