class Config(object):
  DEBUG = False
  TESTING = False
  CSRF_ENABLED = True
  SECRET_KEY = "this-really-needs-to-be-changed"
  SQLALCHEMY_DATABASE_URI = "sqlite:///courses.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  RESTX_ERROR_404_HELP = False

class ProductionConfig(Config):
  DEBUG = False

class StagingConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class DevelopmentConfig(Config):
  DEVELOPMENT = True
  DEBUG = True

class TestingConfig(Config):
  TESTING = True