from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests
import os
import json

API_ENDPOINT =  os.environ['API_ENDPOINT']

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('task')

class Ping(Resource):
    def get(self):
        return {'response': 'ok'}

class TodoList(Resource):
    def get(self):
        print(f'{API_ENDPOINT}/todos')
        r = requests.get(url = f'{API_ENDPOINT}/todos')
        return r.json()

    def post(self):
        args = parser.parse_args()
        r = requests.post(url, json=args)
        return r.json(), 201

class Todo(Resource):
    def get(self, todo_id):
        r = requests.get(url = f'{API_ENDPOINT}/todos/{todo_id}')
        return r.json()

    def delete(self, todo_id):
        r = requests.delete(url = f'{API_ENDPOINT}/todos/{todo_id}')
        return r.json(), 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        r = requests.put(url = f'{API_ENDPOINT}/todos/{todo_id}', json=task)
        return r.json(), 201

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
