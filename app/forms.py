from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, StringField, BooleanField, DateField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import date
from wtforms.validators import ValidationError, DataRequired, NumberRange, Optional,  Regexp, URL
from wtforms.fields import DateTimeLocalField
from flask_wtf.file import FileField, FileAllowed, FileRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('startup', 'Startup'), ('investor', 'Investor'), ('mentor', 'Mentor'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField('Login')

class EditProfileForm(FlaskForm):
    username = StringField('Username')
    bio = TextAreaField('Bio')
    company_name = StringField('Company Name (For Startups)')
    industry = StringField('Industry')
    contact_info = StringField('Contact Info')
    linkedin_profile = StringField('LinkedIn Profile')
    submit = SubmitField('Update Profile')


class MentorshipForm(FlaskForm):
    mentor_id = SelectField('Select Mentor', coerce=int, validators=[DataRequired()])
    date = DateTimeLocalField('Session Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Request Mentorship')


class SearchForm(FlaskForm):
    search_query = StringField('Search', validators=[DataRequired()])
    filter_by = SelectField('Filter By', choices=[
        ('all', 'All'),
        ('startups', 'Startups'),
        ('investors', 'Investors'),
        ('mentors', 'Mentors')
    ])
    submit = SubmitField('Search')


class StartupForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    logo = FileField('Upload Logo', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    clear_logo = BooleanField('Clear current logo')

    industry = StringField('Industry')
    location = StringField('Location')
    founding_date = DateField('Founding Date', format='%Y-%m-%d', validators=[Optional()])
    team_size = IntegerField('Team Size', validators=[Optional()])

    revenue_streams = TextAreaField('Revenue Streams')
    pricing_strategy = TextAreaField('Pricing Strategy')
    customer_acquisition_cost = FloatField('Customer Acquisition Cost', validators=[Optional()])

    stage = SelectField('Funding Stage', choices=[
        ('Pre-Seed', 'Pre-Seed'), 
        ('Seed', 'Seed'),
        ('Pre-Series A', 'Pre-Series A'),
        ('Series A', 'Series A'),
        ('Series B', 'Series B'),
        ('Growth Stage', 'Growth Stage')
    ])

    funding_needed = FloatField('Funding Needed (KES)', validators=[Optional(), NumberRange(min=0)])
    valuation = FloatField('Current Valuation', validators=[Optional(), NumberRange(min=0)])
    previous_funding = TextAreaField('Previous Funding History')

    revenue = FloatField('Current Revenue', validators=[Optional(), NumberRange(min=0)])
    mrr = FloatField('Monthly Recurring Revenue (MRR)', validators=[Optional(), NumberRange(min=0)])
    user_growth = FloatField('User Growth (%)', validators=[Optional(), NumberRange(min=0)])
    partnerships = TextAreaField('Strategic Partnerships')

    tech_stack = TextAreaField('Tech Stack')
    ip_rights = TextAreaField('IP Rights (Patents, Trademarks)')
    competitive_advantage = TextAreaField('Competitive Advantage')

    tam = FloatField('Total Addressable Market (TAM)', validators=[Optional(), NumberRange(min=0)])
    sam = FloatField('Serviceable Available Market (SAM)', validators=[Optional(), NumberRange(min=0)])
    competition = TextAreaField('Competitors / Market Comparison')

    pitch_deck = FileField('Upload Pitch Deck', validators=[FileAllowed(['pdf'])])
    clear_pitch_deck = BooleanField('Clear pitch deck')

    demo_video = FileField('Upload Demo Video', validators=[FileAllowed(['mp4', 'mov'])])
    clear_demo_video = BooleanField('Clear demo video')

    website = StringField('Website')
    social_links = TextAreaField('Social Media Links (one per line)')

    phone_number = StringField('Phone Number', validators=[
        Optional(),
        Regexp(r'^\+?2547\d{8}$', message="Enter a valid Kenyan phone number starting with +2547...")
    ], render_kw={"placeholder": "+254712345678"})

    whatsapp = StringField('WhatsApp Number', validators=[
        Optional(),
        Regexp(r'^\d{10,15}$', message="Enter WhatsApp number without + or spaces (e.g., 254712345678)" )
    ], render_kw={"placeholder": "254712345678"})

    instagram = StringField('Instagram Profile', validators=[Optional()],
        render_kw={"placeholder": "https://instagram.com/yourprofile"})

    facebook = StringField('Facebook Profile', validators=[Optional()],
        render_kw={"placeholder": "https://facebook.com/yourpage"})

    twitter_x = StringField('X (Twitter) Profile', validators=[Optional()],
        render_kw={"placeholder": "https://twitter.com/yourhandle"})

    linkedin = StringField('LinkedIn Profile', validators=[Optional()],
        render_kw={"placeholder": "https://linkedin.com/in/yourprofile"})


    description = TextAreaField('Description')

    submit = SubmitField('Save Startup Details')


class InvestorForm(FlaskForm):
    firm_name = StringField('Firm Name', validators=[Optional()])
    location = StringField('Location', validators=[Optional()])

    check_size_min = FloatField('Minimum Check Size (KES)', validators=[Optional(), NumberRange(min=0)])
    check_size_max = FloatField('Maximum Check Size (KES)', validators=[Optional(), NumberRange(min=0)])

    industry_focus = StringField('Industry Focus', validators=[Optional()])
    stage_focus = SelectField('Preferred Stage', choices=[
        ('pre-seed', 'Pre-Seed'),
        ('seed', 'Seed'),
        ('series-a', 'Series A'),
        ('series-b', 'Series B'),
        ('growth', 'Growth Stage')
    ], validators=[Optional()])

    portfolio = TextAreaField('Portfolio (e.g., past/current startups)', validators=[Optional()])
    deal_preferences = SelectField('Deal Preferences', choices=[
        ('equity', 'Equity'),
        ('debt', 'Debt'),
        ('convertible_note', 'Convertible Note'),
        ('safe', 'SAFE'),
    ], validators=[Optional()])

    investment_thesis = TextAreaField('Investment Thesis', validators=[Optional()])
    engagement_style = SelectField('Engagement Style', choices=[
        ('hands-on', 'Hands-On'),
        ('passive', 'Passive'),
    ], validators=[Optional()])

    past_exits = TextAreaField('Past Exits or Notable Wins', validators=[Optional()])

    submit = SubmitField('Save Investor Profile')


class MentorForm(FlaskForm):
    expertise = TextAreaField('Expertise')
    years_experience = IntegerField('Years of Experience')
    industry_focus = StringField('Industry Focus')
    mentorship_topics = TextAreaField('Preferred Mentorship Topics')
    availability = StringField('General Availability')
    submit = SubmitField('Update Profile')


class MatchingFeedbackForm(FlaskForm):
    score = IntegerField('How would you rate your matches? (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Any feedback or suggestions?', validators=[Optional(), Length(min=5)])
    submit = SubmitField('Submit Feedback')
