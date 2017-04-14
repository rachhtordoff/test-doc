from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
userdocuments = Table('userdocuments', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('document_name', VARCHAR(length=64)),
    Column('user_id', INTEGER),
    Column('required', BOOLEAN),
    Column('uploaded', BOOLEAN),
    Column('accepted', BOOLEAN),
    Column('notes', VARCHAR(length=64)),
    Column('document_type', INTEGER),
)

documentstatus = Table('documentstatus', post_meta,
    Column('user_id', Integer),
    Column('document_type_id', Integer),
    Column('status', String(length=64)),
    Column('id', Integer, primary_key=True, nullable=False),
)

uploadeddocument = Table('uploadeddocument', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('document_name', String(length=64)),
    Column('user_id', Integer),
    Column('document_type_id', Integer),
)

documenttype = Table('documenttype', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('document_type', String(length=64)),
    Column('notes', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['userdocuments'].drop()
    post_meta.tables['documentstatus'].create()
    post_meta.tables['uploadeddocument'].create()
    post_meta.tables['documenttype'].columns['notes'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['userdocuments'].create()
    post_meta.tables['documentstatus'].drop()
    post_meta.tables['uploadeddocument'].drop()
    post_meta.tables['documenttype'].columns['notes'].drop()
