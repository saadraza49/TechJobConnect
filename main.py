# main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db import SessionLocal
import models
from pydantic import BaseModel

app = FastAPI(title="TechJobConnect")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Mock Auth Endpoints
class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str

@app.post("/auth/login")
async def login(req: LoginRequest):
    if req.password == "wrong":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Mocking standard logic based on email domain
    role = "employer" if "employer" in req.email else "job_seeker"
    return {"access_token": "mock-token-123", "role": role}

@app.post("/auth/signup")
async def signup(req: SignupRequest):
    return {"status": "success", "role": req.role}

# Example: Upload CV endpoint
@app.post("/apply/{job_id}")
async def apply_job(job_id: int, cv: UploadFile = File(...), cover_letter: str = None, db: Session = Depends(get_db)):
    # In a real app we'd save it locally or to S3
    return {"info": f"CV {cv.filename} uploaded for job {job_id}", "status": "Applied"}

# Mount the static directory for the frontend (must be last)
app.mount("/", StaticFiles(directory="static", html=True), name="static")