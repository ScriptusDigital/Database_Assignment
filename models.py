from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy 
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()   

#===USER REGISTRATION AND LOGIN MODELS===#
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#===LINK USER TO EXPENSE===#
    expenses = db.relationship(
        'Expense', 
        backref='user', 
        lazy=True,
        cascade='all, delete-orphan',
        )
    
#===LINK USER TO Assignment===#
    assignments = db.relationship(
        'Assignment', 
        backref='user', 
        lazy=True,
        cascade='all, delete-orphan',
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
 #===USER ASSIGNMENTS MODEL===#

class Assignment(db.Model):
    __tablename__ = "assignments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    module_name = db.Column(db.String(120), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(30), default="Medium", nullable=False)
    status = db.Column(db.String(30), default="Not started", nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    def __repr__(self):
        return f"<Assignment {self.title}>"
    
#===USER EXPENSE MODEL===#

class Expense(db.Model):
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Expense {self.amount} - {self.category}>'
    


 #===USER ASSIGNMENTS MODEL===#
