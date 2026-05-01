import flask

def render_main():
    return flask.render_template('main.html')

def render_login():
    return flask.render_template('login.html')