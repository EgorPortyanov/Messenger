import os, dotenv

def get_env(key):
    path = os.path.abspath(os.path.join(__file__, '..', "..", '.env'))
    return dotenv.get_key(path, key)

def migrate():
    os.system("flask db init")
    os.system("flask db migrate")
    os.system("flask db upgrade")