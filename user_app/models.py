from project.db import DATA_BASE 
import flask_login

class User(DATA_BASE.Model, flask_login.UserMixin):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key = True)
    password = DATA_BASE.Column(DATA_BASE.String)
    username = DATA_BASE.Column(DATA_BASE.String)
    email = DATA_BASE.Column(DATA_BASE.String, unique=True)