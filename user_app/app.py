import flask

user_app = flask.Blueprint(
    import_name="user_app", 
    name="user_app", 
    template_folder="templates", 
    static_folder="static",
    static_url_path="/user_app/static"
    )