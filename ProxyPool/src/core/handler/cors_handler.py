# encoding:utf-8
from flask_cors import CORS


def init(app):
    CORS(app, supports_credentials=True)
