from flask_script import Manager
from app import create_app

manager = Manager(create_app)

if __name__ == "__main__":
    # python manage.py                      # shows available commands
    # python manage.py runserver --help     # shows available runserver options
    manager.run()
