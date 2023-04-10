from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
"""Import controllers"""
from controllers.v1 import data_controller
