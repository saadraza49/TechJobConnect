from db import engine
import sqlalchemy

with engine.connect() as conn:
    result = conn.execute(sqlalchemy.text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users';"))
    for row in result:
        print(row)
