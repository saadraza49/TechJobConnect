from db import engine
import sqlalchemy

with engine.connect() as conn:
    print("Tables in public schema:")
    result = conn.execute(sqlalchemy.text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
    for row in result:
        print(row)
