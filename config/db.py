# Python
import json

# SQLAlchemy
from sqlalchemy import create_engine, MetaData

with open('config/db_config.json', mode='r', encoding='utf-8') as f:
    results = json.loads(f.read())
    user = results['user']
    password = results['password']
    host = results['host']
    port = results['port']
    db_name = results['db_name']

engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')

meta = MetaData()

conn = engine.connect()