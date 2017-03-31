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
SECURE_API_URL = os.environ['SECURE_API_URL']
