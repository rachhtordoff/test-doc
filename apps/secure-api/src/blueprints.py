# Import every blueprint file
from src.views import general, user, documents, events, document_name, document_status, document_type, document_notes, document_notification



def register_blueprints(app):
    """
    Adds all blueprint objects into the app.
    """
    app.register_blueprint(general.general)
    app.register_blueprint(user.user)
    app.register_blueprint(events.events)
    app.register_blueprint(documents.documents)
    app.register_blueprint(document_name.document_name)
    app.register_blueprint(document_status.document_status)
    app.register_blueprint(document_type.document_type)
    app.register_blueprint(document_notes.document_notes)
    app.register_blueprint(document_notification.document_notification)

    # All done!
    app.logger.info("Blueprints registered")
