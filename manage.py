from project import project, socketio
from project.db import DATA_BASE

def main():
    with project.app_context():
        DATA_BASE.create_all()
    socketio.run(app=project, port=5001, debug=True)

if __name__ == "__main__":
    main()