from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
userevent = Table('userevent', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('event_name', VARCHAR(length=64)),
    Column('event_date', TIMESTAMP),
    Column('event_description', VARCHAR(length=64)),
    Column('user_id', INTEGER),
)

userdocuments = Table('userdocuments', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('document_name', VARCHAR(length=64)),
    Column('user_id', INTEGER),
    Column('required', BOOLEAN),
    Column('accepted', BOOLEAN),
    Column('uploaded', BOOLEAN),
    Column('notes', VARCHAR(length=64)),
)

userdocuments = Table('userdocuments', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('document_name', String(length=64)),
    Column('user_id', Integer),
    Column('required', Boolean, default=ColumnDefault(False)),
    Column('uploaded', Boolean, default=ColumnDefault(False)),
    Column('accepted', Boolean, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['userevent'].drop()
    pre_meta.tables['userdocuments'].columns['document'].drop()
    post_meta.tables['userdocuments'].columns['accepted'].create()
    post_meta.tables['userdocuments'].columns['document_name'].create()
    post_meta.tables['userdocuments'].columns['required'].create()
    post_meta.tables['userdocuments'].columns['uploaded'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['userevent'].create()
    pre_meta.tables['userdocuments'].columns['document'].create()
    post_meta.tables['userdocuments'].columns['accepted'].drop()
    post_meta.tables['userdocuments'].columns['document_name'].drop()
    post_meta.tables['userdocuments'].columns['required'].drop()
    post_meta.tables['userdocuments'].columns['uploaded'].drop()
