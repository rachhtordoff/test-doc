import os
# For logging

FLASK_LOG_LEVEL = os.environ['LOG_LEVEL']
# For health route
COMMIT = os.environ['COMMIT']
# This APP_NAME variable is to allow changing the app name when the app is running in a cluster. So that
# each app in the cluster will have a unique name.
APP_NAME = os.environ['APP_NAME']

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']

SQLALCHEMY_MIGRATE_REPO = os.environ['SQLALCHEMY_MIGRATE_REPO']

SQLALCHEMY_USER = os.environ['SQLALCHEMY_USER']
SQLALCHEMY_PASSWORD = os.environ['SQLALCHEMY_PASSWORD']
SQLALCHEMY_HOST = os.environ['SQLALCHEMY_HOST']
SQLALCHEMY_PORT = os.environ['SQLALCHEMY_PORT']
SQLALCHEMY_DB = os.environ['SQLALCHEMY_DB']
postgresql_string = 'postgresql://{}:{}@{}:{}/{}'
SQLALCHEMY_DATABASE_URI = postgresql_string.format(SQLALCHEMY_USER, SQLALCHEMY_PASSWORD, SQLALCHEMY_HOST, SQLALCHEMY_PORT, SQLALCHEMY_DB)

aws_access_key_id = os.environ['ACCESS_KEY']
aws_secret_access_key = os.environ['SECRET_KEY']
