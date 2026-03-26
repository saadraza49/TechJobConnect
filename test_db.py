from db import SessionLocal, engine
import models

print("Connecting to DB...")
db = SessionLocal()
print("Executing query...")
models.Base.metadata.create_all(bind=engine)
user = db.query(models.User).first()
print("Query done.")
print(user)
