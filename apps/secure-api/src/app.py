from flask import Flask, g, request
from flask.ext.sqlalchemy import SQLAlchemy
import uuid
import requests

app = Flask(__name__)

app.config.from_pyfile("config.py")
app.config['SQLALCHEMY_POOL_SIZE'] = 100

db = SQLAlchemy(app)

from src import models
