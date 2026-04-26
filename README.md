# TechJobConnect 🚀

TechJobConnect is a modern, full-stack tech job portal and community platform. It bridges the gap between job seekers and employers with a seamless, secure, and interactive experience. Built with a high-performance **FastAPI** backend and a responsive **HTML/CSS/JS** frontend.

## ✨ Key Features

### 🔐 Secure Authentication
- **OTP Verification:** Secure signup process using email OTP (One-Time Password) to verify user identity.
- **Hashed Passwords:** Industry-standard password hashing using `PBKDF2`.
- **JWT Auth:** Secure session management with JSON Web Tokens.
- **Role-Based Access:** Distinct experiences for **Job Seekers** and **Employers**.

### 💼 Job Portal
- **Employer Dashboard:** Post jobs with detailed descriptions and categories.
- **Job Seeker Experience:** Browse the latest job openings.
- **CV Applications:** Apply for jobs directly with file uploads (PDF/Images).
- **Application Tracking:** Real-time notifications for employers when a new application is received.

### 🌐 Community Social Feed
- **Interactive Feed:** Users can share updates, thoughts, and career milestones.
- **Micro-interactions:** Like and comment on posts to engage with the community.
- **Follow System:** Build your professional network by following other users.
- **Personalized Dashboards:** Track your followers, following count, and post activity.

### 🔔 Real-Time Notifications
- Get notified instantly for likes, comments, new followers, and job applications.

---

## 🛠️ Tech Stack

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database:** [PostgreSQL](https://www.postgresql.org/) (via Neon Tech)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Frontend:** Pure HTML5, Vanilla CSS3, and JavaScript (ES6+)
- **Mailing:** `fastapi-mail` for SMTP integration
- **Security:** `passlib` for hashing and `python-jose` for JWT tokens

---

## 📂 Project Structure

```text
├── static/              # Frontend assets (HTML, CSS, JS)
├── uploads/             # User uploaded CVs and documents
├── main.py              # FastAPI application & API routes
├── models.py            # SQLAlchemy database models
├── db.py                # Database connection & configuration
├── requirements.txt     # Python dependencies
└── ...                  # Utility & Migration scripts
```

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/saadraza49/TechJobConnect.git
cd TechJobConnect
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file or set the following environment variables:
- `DATABASE_URL`: Your PostgreSQL connection string.
- `MAIL_USERNAME`: SMTP email address.
- `MAIL_PASSWORD`: SMTP app password.
- `SECRET_KEY`: Random string for JWT signing.

### 5. Run the Application
```bash
uvicorn main:app --reload
```
The app will be available at `http://127.0.0.1:8000`.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License.
