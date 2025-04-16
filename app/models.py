from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))# The Flask-Login



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='startup')
    bio = db.Column(db.Text, nullable=True)  
    company_name = db.Column(db.String(100), nullable=True)  
    industry = db.Column(db.String(50), nullable=True)  
    contact_info = db.Column(db.String(100), nullable=True)  
    linkedin_profile = db.Column(db.String(200), nullable=True)  
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)  
    #def __repr__(self):
     #   return f"User('{self.username}', '{self.email}', '{self.role}')"

    def is_admin(self):
        return self.role == 'admin'

    def is_startup(self):
        return self.role == 'startup'

    def is_investor(self):
        return self.role == 'investor'

    def is_mentor(self):
        return self.role == 'mentor'


class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    funding_needed = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    investment_range_min = db.Column(db.Integer, nullable=False)
    investment_range_max = db.Column(db.Integer, nullable=False)
    industry_focus = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)


class MentorshipSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    startup_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")  # Pending, Approved, Completed

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    target_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
