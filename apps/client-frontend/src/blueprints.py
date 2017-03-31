# Import every blueprint file
from src.views import general, users, documents, events

def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(users.users)
    app.register_blueprint(documents.documents)
    app.register_blueprint(events.events)
    # All done!
    app.logger.info("Blueprints registered")
