from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print("Hashing password...")
try:
    hashed = pwd_context.hash("password123")
    print("Hash successful:", hashed)
except Exception as e:
    print("Error:", e)
