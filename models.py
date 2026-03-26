# Models

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)
    profile = relationship("UserProfile", back_populates="user", uselist=False)

class OTP(Base):
    __tablename__ = "otps"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    otp_code = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    categories = Column(Text)  # store as comma-separated for simplicity
    experience = Column(String)
    preferences = Column(Text)
    resume_url = Column(String)
    portfolio_links = Column(Text)
    user = relationship("User", back_populates="profile")

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    experience = Column(String)
    work_type = Column(String)
    employer_id = Column(Integer, ForeignKey("users.id"))
    deadline = Column(DateTime)

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    job_seeker_id = Column(Integer, ForeignKey("users.id"))
    cv_url = Column(String, nullable=False)
    cover_letter = Column(Text)
    portfolio_links = Column(Text)
    answers = Column(Text)  # can store JSON as string
    status = Column(Enum("Applied", "Viewed", "Shortlisted", "Rejected", name="application_status"))
    applied_at = Column(DateTime, default=datetime.utcnow)