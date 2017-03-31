# This file is the entry point.
# First we import the app object, which will get initialised as we do it. Then import methods we're about to use.
from src.app import app
from src.blueprints import register_blueprints
from src.exceptions import register_exception_handlers

# Register the exception handlers
register_exception_handlers(app)
# Finally we register our blueprints to get our routes up and running.
register_blueprints(app)
