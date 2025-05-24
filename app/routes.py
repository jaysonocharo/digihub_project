from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Startup, Investor, Notification
from app.utils import save_file
from app.forms import RegistrationForm, LoginForm, MentorshipForm, SearchForm, EditProfileForm, InvestorForm, StartupForm, MentorForm, MatchingFeedbackForm
from datetime import datetime
from app.models import User, MentorshipSession, ActivityLog, Startup, Investor, db, MentorshipRequest, Mentor, MatchingFeedback
from app.decorators import role_required
from app.matching import match_startups_to_investors
from app.utils import save_file, delete_file_if_exists, send_notification
from collections import defaultdict
from textblob import TextBlob
routes = Blueprint("routes", __name__)

@routes.route("/")
def home():
    return render_template("home.html")  

@routes.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash(' That email is already registered. Try logging in or resetting your password.', 'danger')
            return redirect(url_for('routes.register'))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # For first admin to be auto-approved
        is_first_admin = form.role.data == 'admin' and not User.query.filter_by(role='admin').first()
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
            approved=(True if is_first_admin or form.role.data != 'admin' else False)
        )

        db.session.add(user)
        db.session.commit()
        flash(f' Account created for {form.username.data}!', 'success')
        return redirect(url_for('routes.login'))

    return render_template('register.html', form=form)


@routes.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            
            if user.role == 'admin' and not user.approved:
                flash('Admin account not approved yet. Please wait for another admin to approve.', 'warning')
                return redirect(url_for('routes.login'))

            login_user(user, remember=form.remember_me.data if hasattr(form, 'remember_me') else False)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('routes.dashboard'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)


@routes.route("/dashboard")
@login_required
def dashboard():
    startup_info = None
    mentorship_requests = []

    if current_user.role == 'startup':
        startup = Startup.query.filter_by(user_id=current_user.id).first()
        if startup:
            startup_info = {
                "logo": url_for('static', filename=startup.logo.replace('\\', '/')) if startup.logo else None,
                "company_name": startup.company_name,
                "industry": startup.industry,
                "profile_link": url_for('routes.view_startup', startup_id=startup.id)
            }
            mentorship_requests = MentorshipRequest.query.filter_by(startup_id=startup.id).all()

    return render_template(
        'dashboard.html',
        user=current_user,
        startup_info=startup_info,
        mentorship_requests=mentorship_requests
    )


@routes.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('routes.home'))

@routes.route("/admin")
@login_required
@role_required('admin')
def admin_home():  
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


@routes.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()

    startup = None
    if current_user.role == 'startup':
        startup = Startup.query.filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.bio = form.bio.data
        current_user.contact_info = form.contact_info.data
        current_user.linkedin_profile = form.linkedin_profile.data

        if startup:
            startup.company_name = form.company_name.data
            startup.industry = form.industry.data
            db.session.commit()
        else:
            db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('routes.profile'))

    # Pre-fill form with existing data
    form.username.data = current_user.username
    form.bio.data = current_user.bio
    form.contact_info.data = current_user.contact_info
    form.linkedin_profile.data = current_user.linkedin_profile
    if startup:
        form.company_name.data = startup.company_name
        form.industry.data = startup.industry

    return render_template('profile.html', form=form)


@routes.route("/matches")
@login_required
def matches():
    if current_user.role not in ['startup', 'investor']:
        abort(403)

    matched_pairs = match_startups_to_investors()
    user_matches = []

    for match in matched_pairs:
        startup = match['startup']
        investor = match['investor']
        score = match['score']
        reasons = match.get('reasons', [])  

        # Filter to only strong matches
        if score >= 70:
            if current_user.role == 'startup' and startup.user_id == current_user.id:
                user_matches.append((startup, investor, score, reasons))
            elif current_user.role == 'investor' and investor.user_id == current_user.id:
                user_matches.append((startup, investor, score, reasons))

    return render_template('matches.html', matches=user_matches)



@routes.route("/mentorship", methods=['GET', 'POST'])
@login_required
def mentorship():
    if current_user.role != 'startup':
        abort(403)  

    form = MentorshipForm()
    form.mentor_id.choices = [(m.id, m.username) for m in User.query.filter_by(role='mentor').all()]

    if form.validate_on_submit():
        print(f" Form validated: Mentor ID={form.mentor_id.data}, Date={form.date.data}")

        session = MentorshipSession(
            mentor_id=form.mentor_id.data,
            startup_id=current_user.id,
            date=form.date.data,
            status="Pending"
        )
        db.session.add(session)
        db.session.commit()

        print(" Session added to database!")

        flash('Mentorship session requested!', 'success')
        return redirect(url_for('routes.mentorship'))

    else:
        print(" Form validation failed. Errors:", form.errors)

    sessions = MentorshipSession.query.filter_by(startup_id=current_user.id).all()
    return render_template('mentorship.html', form=form, sessions=sessions)


@routes.route("/mentor_sessions")
@login_required
def mentor_sessions():
    if current_user.role != 'mentor':
        abort(403)

    mentor = current_user.mentor
    requests = MentorshipRequest.query.filter_by(mentor_id=mentor.id).all()
    return render_template('mentor_sessions.html', requests=requests)


@routes.route("/approve_session/<int:session_id>")
@login_required
def approve_session(session_id):
    session = MentorshipSession.query.get_or_404(session_id)
    if session.mentor_id != current_user.id:
        abort(403)

    session.status = "Approved"
    db.session.commit()

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

    send_notification(session.startup_id, f"Your mentorship session with {current_user.username} has been rejected.")

    flash('Session rejected.', 'danger')
    return redirect(url_for('routes.mentor_sessions'))



@routes.route("/notifications")
@login_required
def notifications():
    page = request.args.get('page', 1, type=int)
    user_notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.timestamp.desc()).paginate(page=page, per_page=10)
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
    startups_query = User.query.filter_by(role='startup')
    investors_query = User.query.filter_by(role='investor')

    startups = startups_query.count()
    investors = investors_query.count()
    mentors = User.query.filter_by(role='mentor').count()
    admins = User.query.filter_by(role='admin').count()
    feedbacks = MatchingFeedback.query.all()

    matches = match_startups_to_investors()
    match_count = len(matches)
    average_score = round(sum(m['score'] for m in matches) / match_count, 2) if matches else 0
    high_quality_matches = sum(1 for m in matches if m['score'] >= 70)
    

    # Match score ranges
    score_ranges = {'0-30': 0, '31-50': 0, '51-70': 0, '71-90': 0, '91-100': 0}
    for match in matches:
        score = match['score']
        if score <= 30:
            score_ranges['0-30'] += 1
        elif score <= 50:
            score_ranges['31-50'] += 1
        elif score <= 70:
            score_ranges['51-70'] += 1
        elif score <= 90:
            score_ranges['71-90'] += 1
        else:
            score_ranges['91-100'] += 1

    # Access related startup/investor profiles
    startup_profiles = [s.startup for s in startups_query if s.startup]
    investor_profiles = [i.investor for i in investors_query if i.investor]
    # Average Funding Needs
    funding_values = [s.funding_needed for s in startup_profiles if s.funding_needed]
    avg_funding_needs = round(sum(funding_values) / len(funding_values), 2) if funding_values else 0
    # Total Valuation
    valuation_values = [s.valuation for s in startup_profiles if s.valuation]
    total_valuation = round(sum(valuation_values), 2)
    # Top Startup Locations
    from collections import Counter
    location_counts = Counter([s.location for s in startup_profiles if s.location])
    top_locations = dict(location_counts.most_common(5))
    # Investor Check Size Histogram (average min/max)
    check_size_data = [
        (inv.check_size_min + inv.check_size_max) / 2
        for inv in investor_profiles
        if inv.check_size_min and inv.check_size_max
    ]

    # Funding Stage Distribution
    stage_counts = Counter([s.stage for s in startup_profiles if s.stage])
    funding_stage_data = dict(stage_counts)
    # Top 5 Strongest Matches
    top_matches = sorted(matches, key=lambda x: x['score'], reverse=True)[:5]
    # Rating distribution
    rating_counts = {i: 0 for i in range(1, 6)}
    for fb in feedbacks:
        if fb.score:
            rating_counts[fb.score] += 1
    # Sentiment analysis
    sentiment_counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}
    for fb in feedbacks:
        if fb.comment:
            blob = TextBlob(fb.comment)
            polarity = blob.sentiment.polarity
            if polarity > 0.1:
                sentiment_counts['Positive'] += 1
            elif polarity < -0.1:
                sentiment_counts['Negative'] += 1
            else:
                sentiment_counts['Neutral'] += 1
    # Matching_feedback
    feedbacks = MatchingFeedback.query.all()
    average_feedback_score = round(sum(f.score for f in feedbacks) / len(feedbacks), 2) if feedbacks else 0
    total_feedback = len(feedbacks)
    recent_comments = [f.comment for f in feedbacks if f.comment]

    return render_template(
        'admin_dashboard.html',
        users=users,
        startups=startups,
        investors=investors,
        mentors=mentors,
        admins=admins,
        match_count=match_count,
        average_score=average_score,
        high_quality_matches=high_quality_matches,
        score_ranges=score_ranges,
        avg_funding_needs=avg_funding_needs,
        total_valuation=total_valuation,
        top_locations=top_locations,
        check_size_data=check_size_data,
        top_matches=top_matches,
        funding_stage_data=funding_stage_data,
        average_feedback_score=average_feedback_score,
        total_feedback=total_feedback,
        recent_comments=recent_comments,
        rating_counts=rating_counts,
        sentiment_counts=sentiment_counts,
    )


@routes.route("/approve_user/<int:user_id>")
@login_required
def approve_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    user.approved = True
    db.session.commit()

    send_notification(user.id, "Your profile has been approved by the DIGIHUB team.", category='system')

    log_action(current_user.id, f"Approved user {user.username}", user.id)

    flash(f'User {user.username} has been approved.', 'success')
    return redirect(url_for('routes.admin_dashboard'))


@routes.route("/ban_user/<int:user_id>")
@login_required
def ban_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)
    user.approved = False  
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


@routes.route('/investor/startups', methods=['GET'])
@login_required
def investor_startups():
    if current_user.role != 'investor':
        abort(403)

    selected_industry = request.args.get('industry')
    selected_stage = request.args.get('stage')
    selected_location = request.args.get('location')

    query = db.session.query(User, Startup).join(Startup, User.id == Startup.user_id)\
        .filter(User.role == 'startup', User.approved == True)

    if selected_industry and selected_industry != 'All':
        query = query.filter(Startup.industry == selected_industry)

    if selected_stage and selected_stage != 'All':
        query = query.filter(Startup.stage == selected_stage)

    if selected_location and selected_location != 'All':
        query = query.filter(Startup.location == selected_location)

    startups = query.all()

    industries = [i[0] for i in db.session.query(Startup.industry).distinct().all() if i[0]]
    stages = [s[0] for s in db.session.query(Startup.stage).distinct().all() if s[0]]
    locations = [l[0] for l in db.session.query(Startup.location).distinct().all() if l[0]]

    return render_template(
        'investor_startups.html',
        startups=startups,
        industries=industries,
        stages=stages,
        locations=locations,
        selected_industry=selected_industry,
        selected_stage=selected_stage,
        selected_location=selected_location
    )

@routes.route('/startup/<int:startup_id>')
@login_required
def view_startup(startup_id):
    startup = Startup.query.get_or_404(startup_id)

    if not startup.user or startup.user.role != 'startup':
        abort(404)

    return render_template('startup_profile.html', user=startup.user, startup=startup)

@routes.route('/startups')
def startups():
    startups = Startup.query.all()
    return render_template('startups.html', startups=startups)

@routes.route("/investor_form", methods=['GET', 'POST'])
@login_required
def investor_form():
    if current_user.role != 'investor':
        abort(403)

    form = InvestorForm()

    existing = Investor.query.filter_by(user_id=current_user.id).first()
    if request.method == 'GET' and existing:
        form.firm_name.data = existing.firm_name
        form.location.data = existing.location
        form.check_size_min.data = existing.check_size_min
        form.check_size_max.data = existing.check_size_max
        form.industry_focus.data = existing.industry_focus
        form.stage_focus.data = existing.stage_focus
        form.portfolio.data = existing.portfolio
        form.deal_preferences.data = existing.deal_preferences
        form.investment_thesis.data = existing.investment_thesis
        form.engagement_style.data = existing.engagement_style
        form.past_exits.data = existing.past_exits

    if form.validate_on_submit():
        if existing:
            investor = existing
        else:
            investor = Investor(user_id=current_user.id)

        investor.firm_name = form.firm_name.data
        investor.location = form.location.data
        investor.check_size_min = form.check_size_min.data
        investor.check_size_max = form.check_size_max.data
        investor.industry_focus = form.industry_focus.data
        investor.stage_focus = form.stage_focus.data
        investor.portfolio = form.portfolio.data
        investor.deal_preferences = form.deal_preferences.data
        investor.investment_thesis = form.investment_thesis.data
        investor.engagement_style = form.engagement_style.data
        investor.past_exits = form.past_exits.data

        db.session.add(investor)
        db.session.commit()

        flash('Investor profile saved successfully!', 'success')
        return redirect(url_for('routes.dashboard'))

    return render_template('investor_form.html', form=form)

def format_social_link(base_url, value):
    if not value:
        return None
    value = value.strip()
    if value.startswith("http"):
        return value
    return base_url + value

@routes.route("/startup_form", methods=['GET', 'POST'])
@login_required
def startup_form():
    if current_user.role != 'startup':
        abort(403)

    form = StartupForm()
    startup = Startup.query.filter_by(user_id=current_user.id).first()

    if form.validate_on_submit():
        print("Form validated!")

        # Create startup if not exists
        if not startup:
            startup = Startup(user_id=current_user.id)
            db.session.add(startup)

        # -- Assigns all fields (excluding files)
        startup.company_name = form.company_name.data
        startup.industry = form.industry.data
        startup.location = form.location.data
        startup.founding_date = form.founding_date.data
        startup.team_size = form.team_size.data
        startup.revenue_streams = form.revenue_streams.data
        startup.pricing_strategy = form.pricing_strategy.data
        startup.customer_acquisition_cost = form.customer_acquisition_cost.data
        startup.stage = form.stage.data
        startup.funding_needed = form.funding_needed.data
        startup.valuation = form.valuation.data
        startup.previous_funding = form.previous_funding.data
        startup.revenue = form.revenue.data
        startup.mrr = form.mrr.data
        startup.user_growth = form.user_growth.data
        startup.partnerships = form.partnerships.data
        startup.tech_stack = form.tech_stack.data
        startup.ip_rights = form.ip_rights.data
        startup.competitive_advantage = form.competitive_advantage.data
        startup.tam = form.tam.data
        startup.sam = form.sam.data
        startup.competition = form.competition.data
        startup.website = form.website.data
        startup.social_links = form.social_links.data
        startup.description = form.description.data

        # -- Contact & Social Link Formatting for validation
        def format_social_link(base_url, value):
            if not value:
                return None
            value = value.strip().lstrip('@')
            if value.startswith("http"):
                return value
            return base_url + value

        if form.phone_number.data:
            startup.phone_number = form.phone_number.data.strip().replace(" ", "")

        if form.whatsapp.data:
            startup.whatsapp = form.whatsapp.data.strip().replace("+", "").replace(" ", "")

        startup.instagram = format_social_link("https://instagram.com/", form.instagram.data)
        startup.facebook = format_social_link("https://facebook.com/", form.facebook.data)
        startup.twitter_x = format_social_link("https://twitter.com/", form.twitter_x.data)
        startup.linkedin = format_social_link("https://linkedin.com/in/", form.linkedin.data)

        # FILE MANAGEMENT(logo, pitch deck, demonstration video)

        # Logo
        if form.clear_logo.data and startup.logo:
            delete_file_if_exists(startup.logo)
            startup.logo = None
        elif form.logo.data:
            if startup.logo:
                delete_file_if_exists(startup.logo)
            startup.logo = save_file(form.logo.data, "logos")
            send_notification(current_user.id, "Your logo was uploaded successfully.", category='media')

        # Pitch Deck
        if form.clear_pitch_deck.data and startup.pitch_deck:
            delete_file_if_exists(startup.pitch_deck)
            startup.pitch_deck = None
        elif form.pitch_deck.data:
            if startup.pitch_deck:
                delete_file_if_exists(startup.pitch_deck)
            startup.pitch_deck = save_file(form.pitch_deck.data, "pitch_decks")
            send_notification(current_user.id, "Your pitch deck was uploaded successfully.", category='media')

        # Demo Video
        if form.clear_demo_video.data and startup.demo_video:
            delete_file_if_exists(startup.demo_video)
            startup.demo_video = None
        elif form.demo_video.data:
            if startup.demo_video:
                delete_file_if_exists(startup.demo_video)
            startup.demo_video = save_file(form.demo_video.data, "demo_videos")
            send_notification(current_user.id, " Your demo video was uploaded successfully.", category='media')

        try:
            db.session.commit()
            flash("Startup profile saved successfully!", "success")
            return redirect(url_for('routes.dashboard'))
        except Exception as e:
            db.session.rollback()
            print(" DB Commit Error:", e)
            flash("An error occurred while saving your data. Please try again.", "danger")

    elif request.method == 'POST':
        print(" Validation failed:", form.errors)

    # Pre-fill values for GET request
    if request.method == 'GET' and startup:
        for field in form:
            if hasattr(startup, field.name):
                setattr(field, 'data', getattr(startup, field.name))

    return render_template("startup_form.html", form=form, startup=startup)


############# MENTOR #############
import spacy
nlp = spacy.load("en_core_web_md")

@routes.route('/mentor_profile/<int:mentor_id>')
@login_required
def mentor_profile(mentor_id):
    mentor = Mentor.query.get_or_404(mentor_id)
    return render_template('mentor_profile.html', mentor=mentor)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@routes.route('/recommended_mentors')
@login_required
def recommended_mentors():
    if current_user.role != 'startup':
        abort(403)

    startup = current_user.startup
    startup_text = " ".join([
        startup.industry or "",
        startup.tech_stack or "",
        startup.competitive_advantage or ""
    ]).strip().lower()

    if not startup_text:
        flash("Please complete your startup profile (e.g. industry, tech stack).")
        return redirect(url_for('routes.dashboard'))

    mentors = Mentor.query.all()
    mentor_data = [(m, (m.expertise or "").strip().lower()) for m in mentors if (m.expertise or "").strip()]

    if not mentor_data:
        flash("No mentors with expertise available.")
        return redirect(url_for('routes.dashboard'))

    doc_startup = nlp(startup_text)
    matches = []

    for mentor, expertise_text in mentor_data:
        doc_mentor = nlp(expertise_text)
        semantic_score = doc_startup.similarity(doc_mentor)  # Semantic similarity (0–1)

        matches.append((mentor, round(semantic_score * 100, 2)))

    # Filter and sort
    top_matches = [match for match in sorted(matches, key=lambda x: x[1], reverse=True) if match[1] > 20]

    return render_template('recommended_mentors.html', matches=top_matches)


from datetime import datetime
from flask import request, redirect, flash

@routes.route('/request_mentorship/<int:mentor_id>', methods=['GET', 'POST'])
@login_required
def request_mentorship(mentor_id):
    if current_user.role != 'startup':
        abort(403)

    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')

        new_request = MentorshipRequest(
            startup_id=current_user.startup.id,
            mentor_id=mentor_id,
            request_date=datetime.strptime(date, "%Y-%m-%d").date(),
            request_time=datetime.strptime(time, "%H:%M").time(),
            status='Pending'
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Mentorship request sent.")
        return redirect(url_for('routes.dashboard'))

    mentor = Mentor.query.get_or_404(mentor_id)
    return render_template('request_mentorship.html', mentor=mentor)


@routes.route('/manage_requests')
@login_required
def manage_requests():
    if current_user.role != 'mentor':
        abort(403)
    mentor = current_user.mentor
    requests = MentorshipRequest.query.filter_by(mentor_id=mentor.id).all()
    return render_template('manage_requests.html', requests=requests)

@routes.route('/update_request/<int:request_id>/<action>')
@login_required
def update_request(request_id, action):
    req = MentorshipRequest.query.get_or_404(request_id)

    if current_user.role != 'mentor' or current_user.mentor.id != req.mentor_id:
        abort(403)

    if action == 'accept':
        req.status = 'Accepted'
        message = f"Your mentorship request for {req.request_date} at {req.request_time.strftime('%H:%M')} was accepted."
    elif action == 'reject':
        req.status = 'Rejected'
        message = f"Your mentorship request for {req.request_date} at {req.request_time.strftime('%H:%M')} was rejected."
    else:
        abort(400)
    db.session.commit()

    # Notify the startup user
    send_notification(req.startup.user_id, message, category='mentorship')

    flash(f"Request has been {req.status.lower()} and startup notified.")
    return redirect(url_for('routes.mentor_sessions'))

@routes.route('/mentor_profile_form', methods=['GET', 'POST'])
@login_required
def mentor_profile_form():
    if current_user.role != 'mentor':
        abort(403)

    mentor = current_user.mentor
    form = MentorForm(obj=mentor)

    if form.validate_on_submit():
        if not mentor:
            mentor = Mentor(user_id=current_user.id)
            db.session.add(mentor)

        form.populate_obj(mentor)
        db.session.commit()
        flash('Mentor profile updated successfully.')
        return redirect(url_for('routes.dashboard'))

    return render_template('mentor_profile_form.html', form=form)


@routes.route('/match_feedback', methods=['GET', 'POST'])
@login_required
def match_feedback():
    form = MatchingFeedbackForm()
    if form.validate_on_submit():
        feedback = MatchingFeedback(
            user_id=current_user.id,
            score=form.score.data,
            comment=form.comment.data
        )
        db.session.add(feedback)
        db.session.commit()
        flash("Thank you for your feedback on the matching system!", "success")
        return redirect(url_for('routes.matches'))
    return render_template('match_feedback.html', form=form)

### NOTIFICATIONS ###
@routes.route("/notifications/mark_read/<int:notification_id>")
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    if notification.user_id != current_user.id:
        abort(403)
    notification.is_read = True
    db.session.commit()
    return redirect(url_for('routes.notifications'))



