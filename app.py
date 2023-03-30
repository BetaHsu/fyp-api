from flask import Flask

app = Flask(__name__)

"""Import controllers"""
from controllers.v1 import data_controller
