from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='startup')
    approved = db.Column(db.Boolean, default=False)

    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(120))  # Filepath or URL
    linkedin_profile = db.Column(db.String(200))
    contact_info = db.Column(db.String(200))

    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    startup = db.relationship('Startup', backref='user', uselist=False)
    investor = db.relationship('Investor', backref='user', uselist=False)
    mentor = db.relationship('Mentor', backref='user', uselist=False)

    def is_admin(self): return self.role == 'admin'
    def is_startup(self): return self.role == 'startup'
    def is_investor(self): return self.role == 'investor'
    def is_mentor(self): return self.role == 'mentor'


class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    company_name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String(120))  # Optional file path
    industry = db.Column(db.String(50))
    location = db.Column(db.String(100))
    founding_date = db.Column(db.Date)
    team_size = db.Column(db.Integer)

    revenue_streams = db.Column(db.Text)
    pricing_strategy = db.Column(db.Text)
    customer_acquisition_cost = db.Column(db.Float)

    stage = db.Column(db.String(50))  # e.g., Seed, Series A
    funding_needed = db.Column(db.Float)
    valuation = db.Column(db.Float)
    previous_funding = db.Column(db.Text)

    revenue = db.Column(db.Float)
    mrr = db.Column(db.Float)
    user_growth = db.Column(db.Float)
    partnerships = db.Column(db.Text)

    tech_stack = db.Column(db.Text)
    ip_rights = db.Column(db.Text)  # patents/trademarks
    competitive_advantage = db.Column(db.Text)

    tam = db.Column(db.Float)
    sam = db.Column(db.Float)
    competition = db.Column(db.Text)

    pitch_deck = db.Column(db.String(120))  # filepath
    demo_video = db.Column(db.String(120))  # filepath or video URL
    website = db.Column(db.String(200))
    social_links = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    firm_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    check_size_min = db.Column(db.Float)
    check_size_max = db.Column(db.Float)
    industry_focus = db.Column(db.String(100))
    stage_focus = db.Column(db.String(100))  # Pre-seed to Series B, etc.

    portfolio = db.Column(db.Text)
    deal_preferences = db.Column(db.String(100))  # Equity, Debt, etc.
    investment_thesis = db.Column(db.Text)
    engagement_style = db.Column(db.String(100))  # Hands-on/passive
    past_exits = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class MentorshipSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    startup_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="Pending")


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

class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    expertise = db.Column(db.Text)
    years_experience = db.Column(db.Integer)
    industry_focus = db.Column(db.String(120))
    mentorship_topics = db.Column(db.Text)
    availability = db.Column(db.String(120))
    
class MentorshipRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    startup_id = db.Column(db.Integer, db.ForeignKey('startup.id'))
    mentor_id = db.Column(db.Integer, db.ForeignKey('mentor.id'))
    request_date = db.Column(db.Date)
    request_time = db.Column(db.Time)
    status = db.Column(db.String(50), default='Pending')  # 'Pending', 'Accepted', 'Rejected'

    startup = db.relationship('Startup', backref='mentorship_requests')
    mentor = db.relationship('Mentor', backref='mentorship_requests')
