from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, BackgroundTasks, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import secrets
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
import os

app = FastAPI(title="TechJobConnect")

# Optional: Drops all tables and recreate to ensure schema changes apply cleanly
# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# --- JWT Configuration ---
SECRET_KEY = os.getenv("SECRET_KEY", "b3a1d95c479e0a2f7c6b813f41a87e2b1029c7b98d3e23ff5b4c1042a9b24e6a")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Email Configuration ---
# NOTE: User must replace these with real credentials to send real emails
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "msaadraza49@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "fugn ckee dcns ausz"),
    MAIL_FROM=os.getenv("MAIL_FROM", "TechJobConnect <msaadraza49@gmail.com>"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,  # Port 465 requires True, Port 587 requires STARTTLS=True/SSL_TLS=False
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)
# Fixed port for 587 configuration
conf.MAIL_STARTTLS = True
conf.MAIL_SSL_TLS = False


class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp_code: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/signup")
async def signup(req: SignupRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if len(req.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    # Check if user exists
    user_exists = db.query(models.User).filter(models.User.email == req.email).first()
    if user_exists:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    otp_code = "".join([str(secrets.randbelow(10)) for _ in range(6)])
    hashed_pwd = pwd_context.hash(req.password)
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    
    # Upsert OTP
    existing_otp = db.query(models.OTP).filter(models.OTP.email == req.email).first()
    if existing_otp:
        existing_otp.otp_code = otp_code
        existing_otp.expires_at = expires_at
        existing_otp.first_name = req.first_name
        existing_otp.last_name = req.last_name
        existing_otp.role = req.role
        existing_otp.password_hash = hashed_pwd
    else:
        new_otp = models.OTP(
            email=req.email,
            otp_code=otp_code,
            expires_at=expires_at,
            first_name=req.first_name,
            last_name=req.last_name,
            role=req.role,
            password_hash=hashed_pwd
        )
        db.add(new_otp)
    db.commit()
    
    # Send email
    message = MessageSchema(
        subject="Your TechJobConnect OTP Code",
        recipients=[req.email],
        body=f"Hello {req.first_name},\n\nYour OTP code to complete registration is: {otp_code}\n\nThis code expires in 10 minutes.",
        subtype=MessageType.plain
    )
    fm = FastMail(conf)
    
    # FastMail will attempt to send email; if email auth fails (dummy creds), 
    # the background task will catch the error in console. 
    # For development without internet/creds, the OTP will just be logged.
    print(f"DEVELOPMENT MODE: Generated OTP for {req.email} is {otp_code}")
    try:
        if conf.MAIL_USERNAME != "your_gmail@gmail.com":
            background_tasks.add_task(fm.send_message, message)
    except Exception as e:
        print(f"Error putting mail task in background: {e}")

    return {"message": "OTP generated. Please check your email to verify."}

@app.post("/verify-otp")
async def verify_otp(req: VerifyOTPRequest, db: Session = Depends(get_db)):
    otp_record = db.query(models.OTP).filter(models.OTP.email == req.email).first()
    
    if not otp_record:
        raise HTTPException(status_code=400, detail="No pending signup found for this email")
        
    if otp_record.otp_code != req.otp_code:
        raise HTTPException(status_code=400, detail="Invalid OTP code")
        
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(status_code=400, detail="OTP has expired")
        
    # Create final user
    new_user = models.User(
        first_name=otp_record.first_name,
        last_name=otp_record.last_name,
        email=otp_record.email,
        password_hash=otp_record.password_hash,
        role=otp_record.role
    )
    db.add(new_user)
    db.delete(otp_record)
    db.commit()
    
    return {"message": "Account created successfully", "role": new_user.role}

@app.post("/auth/login")
async def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

@app.get("/profile")
async def get_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Also return counts for the dashboard
    posts_count = db.query(models.Post).filter(models.Post.user_id == current_user.id).count()
    followers_count = db.query(models.Follower).filter(models.Follower.following_id == current_user.id).count()
    following_count = db.query(models.Follower).filter(models.Follower.follower_id == current_user.id).count()
    
    return {
        "id": current_user.id,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role,
        "bio": current_user.bio,
        "avatar_url": current_user.avatar_url,
        "cover_url": current_user.cover_url,
        "posts_count": posts_count,
        "followers_count": followers_count,
        "following_count": following_count
    }

class ProfileUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    bio: str = None
    avatar_url: str = None
    cover_url: str = None

@app.put("/profile/update")
async def update_profile(req: ProfileUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if req.first_name: current_user.first_name = req.first_name
    if req.last_name: current_user.last_name = req.last_name
    if req.bio: current_user.bio = req.bio
    if req.avatar_url: current_user.avatar_url = req.avatar_url
    if req.cover_url: current_user.cover_url = req.cover_url
    db.commit()
    return {"message": "Profile updated successfully"}

# --- Posts & Feed ---
class PostCreate(BaseModel):
    content: str
    category: str = "General"

@app.post("/posts/create")
async def create_post(req: PostCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_post = models.Post(user_id=current_user.id, content=req.content, category=req.category)
    db.add(new_post)
    db.commit()
    return {"message": "Post created successfully"}

@app.get("/posts/feed")
async def get_feed(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Get IDs of people the user follows
    following_ids = db.query(models.Follower.following_id).filter(models.Follower.follower_id == current_user.id).all()
    following_ids = [id[0] for id in following_ids]
    following_ids.append(current_user.id) # Include own posts
    
    posts = db.query(models.Post).filter(models.Post.user_id.in_(following_ids)).order_by(models.Post.created_at.desc()).all()
    
    feed = []
    for post in posts:
        feed.append({
            "id": post.id,
            "content": post.content,
            "category": post.category,
            "likes_count": post.likes_count,
            "created_at": post.created_at,
            "author": {
                "id": post.author.id,
                "name": f"{post.author.first_name} {post.author.last_name}",
                "avatar_url": post.author.avatar_url
            }
        })
    return feed

@app.post("/posts/{post_id}/like")
async def like_post(post_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes_count += 1
    
    # Notification
    if post.user_id != current_user.id:
        notif = models.Notification(
            user_id=post.user_id,
            type="like",
            reference_id=post.id
        )
        db.add(notif)
    
    db.commit()
    return {"message": "Post liked", "likes_count": post.likes_count}

class CommentCreate(BaseModel):
    content: str

@app.post("/posts/{post_id}/comment")
async def comment_on_post(post_id: int, req: CommentCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    new_comment = models.Comment(post_id=post_id, user_id=current_user.id, content=req.content)
    db.add(new_comment)
    
    # Notification
    if post.user_id != current_user.id:
        notif = models.Notification(
            user_id=post.user_id,
            type="comment",
            reference_id=post.id
        )
        db.add(notif)
        
    db.commit()
    return {"message": "Comment added"}

# --- Following System ---
@app.post("/follow/{user_id}")
async def follow_user(user_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself")
    
    existing = db.query(models.Follower).filter(
        models.Follower.follower_id == current_user.id,
        models.Follower.following_id == user_id
    ).first()
    
    if existing:
        return {"message": "Already following"}
    
    new_follow = models.Follower(follower_id=current_user.id, following_id=user_id)
    db.add(new_follow)
    
    # Notification
    notif = models.Notification(
        user_id=user_id,
        type="follow",
        reference_id=current_user.id
    )
    db.add(notif)
    
    db.commit()
    return {"message": "Followed successfully"}

@app.post("/unfollow/{user_id}")
async def unfollow_user(user_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    follow = db.query(models.Follower).filter(
        models.Follower.follower_id == current_user.id,
        models.Follower.following_id == user_id
    ).first()
    
    if not follow:
        return {"message": "Not following this user"}
    
    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed successfully"}

# --- Jobs & Applications ---
class JobCreate(BaseModel):
    title: str
    description: str
    category: str

@app.post("/jobs/create")
async def create_job(req: JobCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "Employer":
        raise HTTPException(status_code=403, detail="Only employers can create jobs")
    
    new_job = models.Job(employer_id=current_user.id, title=req.title, description=req.description, category=req.category)
    db.add(new_job)
    db.commit()
    return {"message": "Job posted successfully"}

@app.get("/jobs")
async def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).order_by(models.Job.created_at.desc()).all()
    return jobs

@app.post("/jobs/{job_id}/apply")
async def apply_job(job_id: int, cv: UploadFile = File(...), current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "Job Seeker":
        raise HTTPException(status_code=403, detail="Only job seekers can apply for jobs")
    
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
        
    # Save CV
    os.makedirs("uploads/cvs", exist_ok=True)
    file_path = f"uploads/cvs/{current_user.id}_{job_id}_{cv.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(await cv.read())
    
    new_app = models.Application(job_id=job_id, user_id=current_user.id, cv_path=file_path)
    db.add(new_app)
    
    # Notification to employer
    notif = models.Notification(
        user_id=job.employer_id,
        type="application",
        reference_id=job.id
    )
    db.add(notif)
    
    db.commit()
    return {"message": "Application submitted successfully"}

# --- Notifications ---
@app.get("/notifications")
async def get_notifications(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    notifs = db.query(models.Notification).filter(models.Notification.user_id == current_user.id).order_by(models.Notification.created_at.desc()).all()
    return notifs

@app.post("/notifications/mark-read/{notif_id}")
async def mark_notification_read(notif_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notif_id, models.Notification.user_id == current_user.id).first()
    if notif:
        notif.read_flag = True
        db.commit()
    return {"message": "Notification marked as read"}

# Mount the static directory for the frontend (must be last)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
# Trigger reload
