from flask.json import JSONEncoder

from bson import ObjectId
from flask import Flask
from flask_cors import CORS

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, ObjectId):
                return str(obj)
        except TypeError:
            pass
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)
"""Import controllers"""
from controllers.v1 import data_controller
