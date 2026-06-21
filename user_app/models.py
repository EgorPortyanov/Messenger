from project.db import DATA_BASE 
import flask_login

class User(DATA_BASE.Model, flask_login.UserMixin):
    id = DATA_BASE.Column(DATA_BASE.Integer, primary_key=True)
    password = DATA_BASE.Column(DATA_BASE.String)
    email = DATA_BASE.Column(DATA_BASE.String, unique=True)
    is_verified = DATA_BASE.Column(DATA_BASE.Boolean, default=False)
    verify_code = DATA_BASE.Column(DATA_BASE.String)
    
    name = DATA_BASE.Column(DATA_BASE.String, default="")
    surname = DATA_BASE.Column(DATA_BASE.String, default="")
    username = DATA_BASE.Column(DATA_BASE.String, default="")
    gender = DATA_BASE.Column(DATA_BASE.String, default="")
    birth_date = DATA_BASE.Column(DATA_BASE.String, default="")