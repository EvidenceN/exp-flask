from flask import Flask
import requests

APP = Flask(__name__)

@APP.route("/")
def home():
    return f"Hello World"