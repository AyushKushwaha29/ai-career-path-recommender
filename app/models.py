from . import db
from datetime import datetime

class UserQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    skills = db.Column(db.String(500))
    predicted_role = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)