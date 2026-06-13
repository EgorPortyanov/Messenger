import flask, flask_socketio

project = flask.Flask(import_name="project", template_folder="templates")
project.config["SECRET_KEY"] = "kavpkwjnpewqnf"

socketio = flask_socketio.SocketIO(project)