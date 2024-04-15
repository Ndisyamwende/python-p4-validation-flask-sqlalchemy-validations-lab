from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import validates
import re

from models import db, Author, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return 'Validations lab'

# Model Validators
class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String, nullable=False)
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not re.match(r'^\d{10}$', phone_number):
            raise ValueError('Phone number must be exactly ten digits.')
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    summary = db.Column(db.String, nullable=True)
    category = db.Column(db.String, nullable=False)
    
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content must be at least 250 characters long.')
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary must be maximum of 250 characters.')
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError('Category must be either Fiction or Non-Fiction.')
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ['Won\'t Believe', 'Secret', 'Top', 'Guess']
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError('Title must contain one of the following: "Won\'t Believe", "Secret", "Top", "Guess"')
        return title

if __name__ == '__main__':
    app.run(port=5555, debug=True)
