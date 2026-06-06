import flask

chat_app = flask.Blueprint(
    import_name="chat_app", 
    name="chat_app", 
    template_folder="templates", 
    static_folder="static",
    static_url_path="/user_app/static"
    )
