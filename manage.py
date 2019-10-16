from flask import Flask
from flask_script import Manager
from app.view import app


manager = Manager(app)


if __name__ == '__main__':
    manager.run()