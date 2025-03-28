from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

db = SQLAlchemy()


class Formula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top_note = db.Column(JSONB, nullable=False) 
    body_note = db.Column(JSONB, nullable=False) 
    base_note = db.Column(JSONB, nullable=False) 
    formulas = db.Column(JSONB, nullable=False) 
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.now().astimezone().tzinfo))

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)  # Unique session for each conversation
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now(datetime.now().astimezone().tzinfo))


class WebsiteContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)  # Store the scraped website content
    created_at = db.Column(db.DateTime, default=datetime.now(datetime.now().astimezone().tzinfo))
