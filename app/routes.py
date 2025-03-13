from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
#from app import app, db, bcrypt
from app import db, bcrypt  # Import only what is needed
from flask_login import login_user, logout_user, login_required, current_user


routes = Blueprint("routes", __name__)


from app.forms import RegistrationForm, LoginForm, MentorshipForm, SearchForm, EditProfileForm
from datetime import datetime
from app.models import User, MentorshipSession, ActivityLog, Startup, Investor
from app.decorators import role_required

@routes.route("/")
def home():
    return render_template("home.html")  

  
#original
@routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('routes.login'))
    return render_template('register.html', form=form)



@routes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("✅ Form submitted successfully!")

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(f"✅ User found: {user.username}, Role: {user.role}")
        else:
            print("❌ User not found in the database.")

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
            flash(f'Welcome back, {user.username}!', 'success')

            print(f"🔄 Redirecting {user.username} to the dashboard...")

            return redirect(url_for('routes.dashboard'))
        else:
            print("❌ Invalid login credentials!")
            flash('Login failed. Please check your email and password.', 'danger')

    else:
        print("❌ Form validation failed:", form.errors)

    return render_template('login.html', form=form)


@routes.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.login'))

@routes.route("/admin")
@login_required
@role_required('admin')
def admin_home():  #changed from admin dashboard
    return render_template('admin.html')

@routes.route("/investor")
@login_required
@role_required('investor')
def investor_dashboard():
    return render_template('investor.html')

@routes.route("/mentor")
@login_required
@role_required('mentor')
def mentor_dashboard():
    return render_template('mentor.html')


#Editprofileroute
@routes.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.company_name = form.company_name.data if current_user.role == 'startup' else None
        current_user.industry = form.industry.data
        current_user.contact_info = form.contact_info.data
        current_user.linkedin_profile = form.linkedin_profile.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('routes.profile'))
    
    form.username.data = current_user.username
    form.bio.data = current_user.bio
    form.company_name.data = current_user.company_name
    form.industry.data = current_user.industry
    form.contact_info.data = current_user.contact_info
    form.linkedin_profile.data = current_user.linkedin_profile
    
    return render_template('profile.html', form=form)

from app.matching import match_startups_to_investors

@routes.route("/matches")
@login_required
def matches():
    if current_user.role != 'investor' and current_user.role != 'startup':
        abort(403)

    matched_pairs = match_startups_to_investors()
    return render_template('matches.html', matches=matched_pairs)



@routes.route("/mentorship", methods=['GET', 'POST'])
@login_required
def mentorship():
    if current_user.role != 'startup':
        abort(403)  # Only startups can request mentorship

    form = MentorshipForm()
    form.mentor_id.choices = [(m.id, m.username) for m in User.query.filter_by(role='mentor').all()]

    if form.validate_on_submit():
        print(f"✅ Form validated: Mentor ID={form.mentor_id.data}, Date={form.date.data}")

        session = MentorshipSession(
            mentor_id=form.mentor_id.data,
            startup_id=current_user.id,
            date=form.date.data,
            status="Pending"
        )
        db.session.add(session)
        db.session.commit()

        print("✅ Session added to database!")

        flash('Mentorship session requested!', 'success')
        return redirect(url_for('routes.mentorship'))

    else:
        print("❌ Form validation failed. Errors:", form.errors)

    sessions = MentorshipSession.query.filter_by(startup_id=current_user.id).all()
    return render_template('mentorship.html', form=form, sessions=sessions)

# @routes.route("/mentorship", methods=['GET', 'POST'])
# @login_required
# def mentorship():
#     if current_user.role != 'startup':
#         abort(403)  # Only startups can request mentorship

#     form = MentorshipForm()
#     form.mentor_id.choices = [(m.id, m.username) for m in User.query.filter_by(role='mentor').all()]

#     if form.validate_on_submit():
#         session = MentorshipSession(
#             mentor_id=form.mentor_id.data,
#             startup_id=current_user.id,
#             date=form.date.data,
#             status="Pending"
#         )
#         db.session.add(session)
#         db.session.commit()
#         flash('Mentorship session requested!', 'success')
#         return redirect(url_for('routes.mentorship'))

#     sessions = MentorshipSession.query.filter_by(startup_id=current_user.id).all()
#     return render_template('mentorship.html', form=form, sessions=sessions)




@routes.route("/mentor_sessions", methods=['GET', 'POST'])
@login_required
def mentor_sessions():
    if current_user.role != 'mentor':
        abort(403)  # Only mentors can access this page

    sessions = MentorshipSession.query.filter_by(mentor_id=current_user.id).all()
    for session in sessions:
        session.startup = User.query.get(session.startup_id)

    return render_template('mentor_sessions.html', sessions=sessions)


@routes.route("/approve_session/<int:session_id>")
@login_required
def approve_session(session_id):
    session = MentorshipSession.query.get_or_404(session_id)
    if session.mentor_id != current_user.id:
        abort(403)

    session.status = "Approved"
    db.session.commit()

            # Send notification to startup
    send_notification(session.startup_id, f"Your mentorship session with {current_user.username} has been approved.")

    flash('Session approved!', 'success')
    return redirect(url_for('routes.mentor_sessions'))

@routes.route("/reject_session/<int:session_id>")
@login_required
def reject_session(session_id):
    session = MentorshipSession.query.get_or_404(session_id)
    if session.mentor_id != current_user.id:
        abort(403)

    session.status = "Rejected"
    db.session.commit()

    # Send notification to startup
    send_notification(session.startup_id, f"Your mentorship session with {current_user.username} has been rejected.")

    flash('Session rejected.', 'danger')
    return redirect(url_for('routes.mentor_sessions'))



from app.models import Notification

def send_notification(user_id, message):
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()


@routes.route("/notifications")
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).all()
    return render_template('notifications.html', notifications=user_notifications)




@routes.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    results = []

    if form.validate_on_submit():
        query = form.search_query.data.lower()
        filter_by = form.filter_by.data

        if filter_by == 'startups':
            results = User.query.filter(User.role == 'startup', User.username.ilike(f"%{query}%")).all()
        elif filter_by == 'investors':
            results = User.query.filter(User.role == 'investor', User.username.ilike(f"%{query}%")).all()
        elif filter_by == 'mentors':
            results = User.query.filter(User.role == 'mentor', User.username.ilike(f"%{query}%")).all()
        else:
            results = User.query.filter(User.username.ilike(f"%{query}%")).all()

    return render_template('search.html', form=form, results=results)



@routes.route("/admin_dashboard")
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)

    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)

@routes.route("/approve_user/<int:user_id>")
@login_required
def approve_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    user.approved = True
    db.session.commit()

    log_action(current_user.id, f"Approved user {user.username}", user.id)

    flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('routes.admin_dashboard'))



@routes.route("/ban_user/<int:user_id>")
@login_required
def ban_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    user.approved = False  # Revoke approval instead of deleting user data
    db.session.commit()

    log_action(current_user.id, f"Banned user {user.username}", user.id)

    flash(f'User {user.username} has been banned.', 'danger')
    return redirect(url_for('routes.admin_dashboard'))

@routes.route("/delete_user/<int:user_id>")
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    log_action(current_user.id, f"Deleted user {user.username}", user.id)

    db.session.delete(user)
    db.session.commit()

    flash(f'User {user.username} has been deleted.', 'danger')
    return redirect(url_for('routes.admin_dashboard'))


def log_action(admin_id, action, target_user_id=None):
    log = ActivityLog(admin_id=admin_id, action=action, target_user_id=target_user_id)
    db.session.add(log)
    db.session.commit()


@routes.route("/activity_logs")
@login_required
def activity_logs():
    if current_user.role != 'admin':
        abort(403)

    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).all()
    return render_template('activity_log.html', logs=logs)


#route for investors to view startups
@routes.route('/investor/startups')
@login_required
def investor_startups():
    if current_user.role != 'investor':
        abort(403)  # Restrict access to only investors

    startups = User.query.filter_by(role='startup', approved=True).all()
    return render_template('investor_startups.html', startups=startups)


#route for viewing individual startups(seeing more detail about a startup)
@routes.route('/startup/<int:startup_id>')
@login_required
def view_startup(startup_id):
    startup = User.query.get_or_404(startup_id)
    if startup.role != 'startup':
        abort(404)

    return render_template('startup_profile.html', startup=startup)


@routes.route('/startups')
def startups():
    startups = Startup.query.all()
    return render_template('startups.html', startups=startups)


