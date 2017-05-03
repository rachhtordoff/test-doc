from src.app import db
from sqlalchemy import create_engine
from src.models import Setup, userdetails, Documentstatus, bucket, uploadedDocument, Documenttype, DocumentNotes

class Sql:
    session = db.create_scoped_session()
#start of search sql statements
    def get_user_login(params):
        return Sql.session.query(Setup).filter_by(**params).all()

    def get_user(params):
        return Sql.session.query(userdetails).filter_by(**params).all()

    def get_bucket(params):
        return Sql.session.query(bucket).filter_by(**params).all()

    def get_all_buckets():
        return Sql.session.query(bucket).all()

    def get_all_types():
        return Sql.session.query(Documenttype).all()

    def get_type(params):
        return Sql.session.query(Documenttype).filter_by(**params).all()

    def get_notes(params):
        return Sql.session.query(DocumentNotes).filter_by(**params).all()

    def get_document_status(params):
        return Sql.session.query(Documentstatus).filter_by(**params).all()

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

    def get_document_name(params):
        return Sql.session.query(uploadedDocument).filter_by(**params).all()

#start of insert sql statments
    def new_usersetup(params):
        try_usersetup = Setup(**params)
        Sql.session.add(try_usersetup)
        Sql.session.commit()
        return Sql.get_user_login(try_usersetup.to_dict())

    def new_document_status(params):
        try_status = Documentstatus(**params)
        Sql.session.add(try_status)
        Sql.session.commit()
        return Sql.get_document_status(try_status.to_dict())

    def new_document_note(params):
        try_note = DocumentNotes(**params)
        Sql.session.add(try_note)
        Sql.session.commit()
        return Sql.get_notes(try_note.to_dict())

    def new_user(params):
        try_user = userdetails(**params)
        Sql.session.add(try_user)
        Sql.session.commit()
        return Sql.get_user(try_user.to_dict())

    def new_document_name(params):
        try_document = uploadedDocument(**params)
        Sql.session.add(try_document)
        Sql.session.commit()
        return Sql.get_document_name(try_document.to_dict())

    def new_bucket(params):
        try_bucket = bucket(**params)
        Sql.session.add(try_bucket)
        Sql.session.commit()
        return Sql.get_bucket(try_bucket.to_dict())

    def new_doc_type(params):
        try_type = Documenttype(**params)
        Sql.session.add(try_type)
        Sql.session.commit()
        return Sql.get_all_types(try_bucket.to_dict())

#start of update sql statments
    def update_user(id, params):
        updating = Sql.session.query(userdetails).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_user({'id':id})

    def update_document_name(id, params):
        updating = Sql.session.query(uploadedDocument).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_document_name({'id':id})

    def update_document_type(id, params):
        updating = Sql.session.query(Documenttype).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_document_type({'id':id})

    def update_document_status(id, params):
        updating = Sql.session.query(Documentstatus).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_document_status({'id':id})


    def update_usersetup(id, params):
        updating = Sql.session.query(Setup).get(id)
        for key, value in params.items():
            setattr(updating, key, value)
        Sql.session.commit()
        return Sql.get_user_login({'id':id})

Sql.session.close()
