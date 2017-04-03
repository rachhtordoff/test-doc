from src.app import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm.session import Session


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


class UserDocument(db.Model):
    __tablename__ = 'userdocuments'

    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer, ForeignKey("userdetails.id"))

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "document" : self.document,
            "user_id" : self.user_id
            }


class UserEvent(db.Model):
    __tablename__ = 'userevent'
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(64))
    event_date = db.Column(db.DateTime)
    event_description = db.Column(db.String(64))
    user_id = db.Column(db.Integer, ForeignKey("userdetails.id"))

    def save(self):  # pragma: no cover
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            "id" : self.id,
            "event_name" : self.event_name,
            "event_date" : self.event_date,
            "event_description" : self.event_description,
            "user_id" : self.user_id
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
