import flask_sqlalchemy
import flask_migrate
from .settings import project

project.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.base'
project.config['SECRET_KEY'] = 'secret_key'

DATA_BASE = flask_sqlalchemy.SQLAlchemy(project)
MIGRATE = flask_migrate.Migrate(project, DATA_BASE)