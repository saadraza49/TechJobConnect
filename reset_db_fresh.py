from db import engine, Base
import models

def reset_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully with new schema.")

if __name__ == "__main__":
    reset_database()
