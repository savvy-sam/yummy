"""This module creates app, an instance of Flask"""
#import Flask class form the flask
from flask import Flask
from app import views

# create an instance of the Flask class
app = Flask(__name__, instance_relative_config=True)
# import views.pys
# Allow app to use comfigurations defined in config.py
app.config.from_object('config')
