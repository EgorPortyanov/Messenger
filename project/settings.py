import flask

project = flask.Flask(import_name="project", template_folder="templates")
project.config["SECRET_KEY"] = "kavpkwjnpewqnf"
