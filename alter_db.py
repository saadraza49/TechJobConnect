from db import engine
import sqlalchemy

print("Adding first_name and last_name columns to users table...")
with engine.connect() as conn:
    try:
        conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN first_name VARCHAR DEFAULT '';"))
        conn.commit()
        print("Added first_name")
    except Exception as e:
        print(f"Error adding first_name: {e}")
        
    try:
        conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN last_name VARCHAR DEFAULT '';"))
        conn.commit()
        print("Added last_name")
    except Exception as e:
        print(f"Error adding last_name: {e}")
        
    try:
        conn.execute(sqlalchemy.text("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR USING role::VARCHAR;"))
        conn.commit()
        print("Changed role to VARCHAR")
    except Exception as e:
        print(f"Error changing role type: {e}")

print("Creating new tables (like otps) if they don't exist...")
import models
models.Base.metadata.create_all(bind=engine)
print("Done!")
