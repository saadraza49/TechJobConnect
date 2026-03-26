from db import engine
import sqlalchemy

print("Adding remaining columns to users table...")
with engine.connect() as conn:
    try:
        conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN password_hash VARCHAR DEFAULT '';"))
        conn.commit()
        print("Added password_hash")
    except Exception as e:
        print(f"Error adding password_hash: {e}")
        
    try:
        conn.execute(sqlalchemy.text("ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'job_seeker';"))
        conn.commit()
        print("Added role")
    except Exception as e:
        print(f"Error adding role: {e}")

print("Done!")
