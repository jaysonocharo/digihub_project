from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, StringField, BooleanField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from datetime import date
from wtforms.validators import ValidationError, DataRequired, NumberRange



#original reg. form
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


# class MentorshipForm(FlaskForm):
#     mentor_id = SelectField('Select Mentor', coerce=int, validators=[DataRequired()])
#     date = DateField('Session Date', format='%Y-%m-%d', validators=[DataRequired()])
#     submit = SubmitField('Request Mentorship')



class MentorshipForm(FlaskForm):
    mentor_id = SelectField('Select Mentor', coerce=int, validators=[DataRequired()])
    date = DateField('Session Date', format='%Y-%m-%d %H:%M', validators=[DataRequired()])
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

#for startup and investor fields
class StartupForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    funding_needed = IntegerField('Funding Needed (KES)', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Startup Details')

class InvestorForm(FlaskForm):
    investment_range_min = IntegerField('Minimum Investment (KES)', validators=[DataRequired()])
    investment_range_max = IntegerField('Maximum Investment (KES)', validators=[DataRequired()])
    industry_focus = StringField('Industry Focus', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Investor Details')

