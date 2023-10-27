# third-party imports
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

# local imports
from .config import DevelopmentConfig


api = Api()
db = SQLAlchemy()

def create_app(config=DevelopmentConfig):
  app = Flask(__name__)
  app.config.from_object(config)

  api.init_app(app, version="1.0", title="Course API", description="A course API")
  db.init_app(app)

  from .resources import student_ns, course_ns
  api.add_namespace(student_ns)
  api.add_namespace(course_ns)

  with app.app_context():
    db.create_all()

  return app