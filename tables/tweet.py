# sqlalchemy
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, DateTime

from config.db import meta, engine

tweets = Table(
    'tweets',
    meta,
    Column(
        'id',
        Integer,
        primary_key=True
    ),
    Column(
        'content',
        String(256)
    ),
    Column(
        'created_at',
        DateTime
    ),
    Column(
        'updated_at',
        DateTime
    ),
    Column(
        'user_id',
        Integer,
        ForeignKey('users.id')
    )
)

meta.create_all(engine)