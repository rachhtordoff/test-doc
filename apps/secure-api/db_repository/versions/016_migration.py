from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
documentnotes = Table('documentnotes', post_meta,
    Column('note', String(length=64)),
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer),
    Column('document_type_id', Integer),
)

documenttype = Table('documenttype', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('document_type', VARCHAR(length=64)),
    Column('notes', VARCHAR(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['documentnotes'].create()
    pre_meta.tables['documenttype'].columns['notes'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['documentnotes'].drop()
    pre_meta.tables['documenttype'].columns['notes'].create()
