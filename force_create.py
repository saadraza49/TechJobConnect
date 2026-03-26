from db import engine
import models
print("Recreating all models...")
models.Base.metadata.create_all(bind=engine)
print("Done. Testing users table...")
from db import SessionLocal
db = SessionLocal()
users = db.query(models.User).all()
print("Success! User count:", len(users))
