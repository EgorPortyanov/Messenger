import flask
from flask_login import LoginManager

project = flask.Flask(import_name="project", template_folder="templates")


project.config["SECRET_KEY"] = "keyqkgnqgnj"