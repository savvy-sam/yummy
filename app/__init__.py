from flask import Flask

app=Flask(__name__, instance_relative_config=True)

from app import view

app.config.from_object('config')