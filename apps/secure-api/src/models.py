from src.app import db
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import relationship



class Setup(db.Model):
    __tablename__ = 'setup'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "username" : self.username
        }


class userdetails(db.Model):
    __tablename__ = 'userdetails'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer,ForeignKey("setup.id"))
    surname = db.Column(db.String(64))
    forname = db.Column(db.String(64))
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String(64))
    complete = db.Column(db.String(64))
    type = db.Column(db.String(64))

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "account_id" : self.account_id,
            "surname" : self.surname,
            "forname" : self.forname,
            "date_of_birth" : self.date_of_birth,
            "gender" : self.gender,
            "complete" : self.complete,
            "type" : self.type
        }


class Documenttype(db.Model):
    __tablename__ = 'documenttype'

    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(64))
    notes =  db.Column(db.String(64))
    documentstatus = db.relationship("Documentstatus", backref=db.backref('documenttype', uselist='false'))
    documentsuploaded = db.relationship("uploadedDocument", backref=db.backref('documenttype', uselist='false'))


    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "document_type" : self.document_type,
            "notes" : self.notes
            }


class uploadedDocument(db.Model):
    __tablename__ = 'uploadeddocument'

    id = db.Column(db.Integer, primary_key=True)
    document_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, ForeignKey("userdetails.id"))
    document_type_id = db.Column(db.Integer, ForeignKey("documenttype.id"))


    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "document_type_id" : self.document_type_id,
            "user_id" : self.user_id,
            "document_name" : self.document_name
            }

    def __repr__(self):
        self.to_dict


class Documentstatus(db.Model):
    __tablename__ = 'documentstatus'

    status = db.Column(db.String(64))
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, ForeignKey("userdetails.id"))
    document_type_id = db.Column(db.Integer, ForeignKey("documenttype.id"))

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()


    def to_dict(self):
        return {
            "user_id" : self.user_id,
            "document_type_id" : self.document_type_id,
            "status" : self.status,
            "id" : self.id
                }


class bucket(db.Model):
    __tablename__ = 'bucket'
    id = db.Column(db.Integer, primary_key=True)
    bucket_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, ForeignKey("userdetails.id"))

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "bucket_name" : self.bucket_name,
            "user_id" : self.user_id
        }
