from db import SessionLocal
import models
print("Connecting...")
db = SessionLocal()
print("Querying users...")
user = db.query(models.User).first()
print("User query complete.")
print(user)
