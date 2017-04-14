from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
documenttype = Table('documenttype', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('document_type', String(length=64)),
)

userdocuments = Table('userdocuments', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('document_name', String(length=64)),
    Column('required', Boolean, default=ColumnDefault(False)),
    Column('uploaded', Boolean, default=ColumnDefault(False)),
    Column('accepted', Boolean, default=ColumnDefault(False)),
    Column('notes', String(length=64)),
    Column('user_id', Integer),
    Column('document_type', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['documenttype'].create()
    post_meta.tables['userdocuments'].columns['document_type'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['documenttype'].drop()
    post_meta.tables['userdocuments'].columns['document_type'].drop()
