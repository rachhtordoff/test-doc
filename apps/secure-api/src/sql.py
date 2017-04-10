from src.app import db
from sqlalchemy import create_engine
from src.models import Setup, userdetails, UserDocument, UserEvent, bucket

class Sql:
    session = db.create_scoped_session()
#start of search sql statements
    def get_user_login(params):
        return Sql.session.query(Setup).filter_by(**params).all()

    def get_user(params):
        return Sql.session.query(userdetails).filter_by(**params).all()

    def get_bucket(params):
        return Sql.session.query(bucket).filter_by(**params).all()


    def get_user_with_details_documents(params):
        user = Sql.session.query(userdetails).filter_by(**params).all()
        result = []
        for user in user:
            user_dict = user.to_dict()
            user_dict['document'] = []

            document_result = Sql.get_user_document({"user_id":user_dict['id']})

            for documents in document_result:
                user_dict['document'].append(documents.to_dict())

            result.append(user_dict)
            return result

    def get_user_document(params):
        return Sql.session.query(UserDocument).filter_by(**params).all()

    def get_user_events(params):
        return Sql.session.query(UserEvent).filter_by(**params).all()

#start of insert sql statments
    def new_usersetup(params):
        try_usersetup = Setup(**params)
        Sql.session.add(try_usersetup)
        Sql.session.commit()
        return Sql.get_user_login(try_usersetup.to_dict())

    def new_user(params):
        try_user = userdetails(**params)
        Sql.session.add(try_user)
        Sql.session.commit()
        return Sql.get_user(try_user.to_dict())

    def new_document(params):
        try_document = UserDocument(**params)
        Sql.session.add(try_document)
        Sql.session.commit()
        return Sql.get_user_document(try_document.to_dict())

    def new_event(params):
        try_event = UserEvent(**params)
        Sql.session.add(try_event)
        Sql.session.commit()
        return Sql.get_user_events(try_event.to_dict())

    def new_bucket(params):
        try_bucket = bucket(**params)
        Sql.session.add(try_bucket)
        Sql.session.commit()
        print(Sql.get_bucket(try_bucket.to_dict()))
        return Sql.get_bucket(try_bucket.to_dict())

#start of update sql statments
    def update_user(id, params):
        updating = Sql.session.query(userdetails).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_user({'id':id})

    def update_usersetup(id, params):
        updating = Sql.session.query(Setup).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_user_login({'id':id})

db.session.close()
