from flask import Flask, request, send_from_directory
from flask_restful import Api, Resource, reqparse
import random
from generation import *

app = Flask(__name__, static_url_path='')
api = Api(app)

class Quote(Resource):
    def get(self):
        drum = request.args.getlist('drum', type=str)[0]
        interpolation = request.args.getlist('interpolation', type=str)
        print(drum)
        path = generate(drum, '', interpolation)
        return send_from_directory('sounds', path)

api.add_resource(Quote, "/generate/")
if __name__ == '__main__':
    app.run(debug=True)






