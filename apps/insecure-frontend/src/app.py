from flask import Flask, g, request
import uuid
import requests

app = Flask(__name__)

app.config.from_pyfile("config.py")
