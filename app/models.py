from . import db
from datetime import datetime

# 1. User Career Queries (from the original feature)
class UserQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    skills = db.Column(db.String(500))
    predicted_role = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# 2. Interview Sessions (New AI Interviewer feature)
class InterviewSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(100))
    level = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)
    feedback = db.Column(db.Text, nullable=True)
    # Relationship to messages
    messages = db.relationship('ChatMessage', backref='session', lazy=True)

# 3. Chat Messages (For the Interview Chat)
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('interview_session.id'), nullable=False)
    sender = db.Column(db.String(10)) # 'AI' or 'User'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)