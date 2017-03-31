# Import every blueprint file
from src.views import general, user, documents, events



def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(user.user)
    app.register_blueprint(events.events)
    app.register_blueprint(documents.documents)

    # All done!
    app.logger.info("Blueprints registered")
