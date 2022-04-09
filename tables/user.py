# sqlalchemy
from sqlalchemy import Integer, Table, Column
from sqlalchemy.sql.sqltypes import String, Date

from config.db import meta, engine

users = Table(
    'users',
    meta,
    Column(
        'id',
        Integer,
        autoincrement=True,
        primary_key=True
    ),
    Column(
        'email',
        String(255)
    ),
    Column(
        'first_name',
        String(50)
    ),
    Column(
        'last_name',
        String(50)
    ),
    Column(
        'birth_date',
        Date
    ),
    Column(
        'password',
        String(255)
    )
)

meta.create_all(engine)