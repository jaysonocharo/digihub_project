import os
import random
from faker import Faker
from datetime import datetime, timedelta
from app import create_app, db
from app.models import User, Startup, Investor, Mentor
import bcrypt

# Setup
app = create_app()
fake = Faker()
app.app_context().push()
db.drop_all()
db.create_all()

# Global password
password = 'test123'
hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Upload folder
UPLOAD_FOLDER = "static/uploads"

# --- 1. Create Admin ---

# --- Add dedicated admin user 'Jayson' ---
jayson_admin = User(
    username='Jayson',
    email='jaysonocharo@students.uonbi.ac.ke',
    password=bcrypt.hashpw('iwzhia_.21'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    role='admin',
    approved=True,
    bio=fake.text(),
    linkedin_profile=fake.url(),
    contact_info=fake.phone_number()
)
db.session.add(jayson_admin)


admin = User(
    username='admin',
    email='admin@example.com',
    password=hashed_pw,
    role='admin',
    approved=True
)
db.session.add(admin)

# --- 2. Create Startups ---
industries = ['FinTech', 'AgriTech', 'HealthTech', 'EdTech', 'E-Commerce']

for i in range(1, 11):
    user = User(
        username=f"startup{i}",
        email=f"startup{i}@test.com",
        password=hashed_pw,
        role='startup',
        approved=True,
        bio=fake.text(),
        linkedin_profile=fake.url(),
        contact_info=fake.phone_number()
    )
    db.session.add(user)
    db.session.flush()  # Get user.id before creating startup

    startup = Startup(
        user_id=user.id,
        company_name=fake.company(),
        logo=f"{UPLOAD_FOLDER}/logo_{i}.png",
        industry=random.choice(industries),
        location=fake.city(),
        founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
        team_size=random.randint(5, 50),
        revenue_streams=fake.text(),
        pricing_strategy=fake.text(),
        customer_acquisition_cost=random.uniform(10, 200),
        stage=random.choice(['Seed', 'Series A', 'Series B']),
        funding_needed=random.uniform(50000, 500000),
        valuation=random.uniform(100000, 5000000),
        previous_funding=fake.sentence(),
        revenue=random.uniform(10000, 500000),
        mrr=random.uniform(1000, 100000),
        user_growth=random.uniform(5, 50),
        partnerships=fake.company(),
        tech_stack=fake.words(nb=3, unique=True),
        ip_rights="None yet",
        competitive_advantage=fake.text(),
        tam=random.uniform(1e6, 1e8),
        sam=random.uniform(1e5, 1e7),
        competition=fake.company(),
        pitch_deck=f"{UPLOAD_FOLDER}/pitch_{i}.pdf",
        demo_video=f"{UPLOAD_FOLDER}/demo_{i}.mp4",
        website=fake.url(),
        social_links=fake.url()
    )
    db.session.add(startup)

# --- 3. Create Investors ---
for i in range(1, 11):
    user = User(
        username=f"investor{i}",
        email=f"investor{i}@test.com",
        password=hashed_pw,
        role='investor',
        approved=True,
        bio=fake.text(),
        linkedin_profile=fake.url(),
        contact_info=fake.phone_number()
    )
    db.session.add(user)
    db.session.flush()

    investor = Investor(
        user_id=user.id,
        firm_name=fake.company(),
        location=fake.city(),
        check_size_min=random.uniform(10000, 50000),
        check_size_max=random.uniform(50000, 500000),
        industry_focus=random.choice(industries),
        stage_focus=random.choice(['Seed', 'Series A', 'Series B']),
        portfolio=fake.text(),
        deal_preferences=random.choice(['Equity', 'Debt', 'SAFE']),
        investment_thesis=fake.text(),
        engagement_style=random.choice(['Hands-on', 'Passive']),
        past_exits=fake.company()
    )
    db.session.add(investor)

# --- 4. Create Mentors ---
for i in range(1, 11):
    user = User(
        username=f"mentor{i}",
        email=f"mentor{i}@test.com",
        password=hashed_pw,
        role='mentor',
        approved=True,
        bio=fake.text(),
        linkedin_profile=fake.url(),
        contact_info=fake.phone_number()
    )
    db.session.add(user)
    db.session.flush()

    mentor = Mentor(
        user_id=user.id,
        expertise=fake.job(),
        years_experience=random.randint(3, 20),
        industry_focus=random.choice(industries),
        mentorship_topics=", ".join(fake.words(nb=3)),
        availability="Weekdays, 9am - 5pm"
    )
    db.session.add(mentor)

# Commit everything
db.session.commit()
print("✅ Seeded 1 admin, 10 startups, 10 investors, and 10 mentors.")



## Seeding mentorship requests and mentorship sessions##

from app import create_app, db
from app.models import Startup, Mentor, MentorshipRequest, MentorshipSession
from faker import Faker
from datetime import datetime, timedelta
import random

# Setup
app = create_app()
app.app_context().push()
fake = Faker()

# --- 1. Seed Mentorship Requests ---

print("🔁 Seeding mentorship requests...")

all_startups = Startup.query.all()
all_mentors = Mentor.query.all()

for startup in all_startups:
    selected_mentors = random.sample(all_mentors, k=2)  # each startup requests from 2 mentors
    for mentor in selected_mentors:
        req_date = fake.date_between(start_date='today', end_date='+30d')
        req_time = (datetime.utcnow() + timedelta(hours=random.randint(9, 17))).time()
        status = random.choice(['Pending', 'Accepted', 'Rejected'])

        mentorship_request = MentorshipRequest(
            startup_id=startup.id,
            mentor_id=mentor.id,
            request_date=req_date,
            request_time=req_time,
            status=status
        )
        db.session.add(mentorship_request)

# --- 2. Seed Mentorship Sessions (only from accepted requests) ---

print("📅 Seeding mentorship sessions from accepted requests...")

accepted_requests = MentorshipRequest.query.filter_by(status='Accepted').all()

for req in accepted_requests:
    session = MentorshipSession(
        mentor_id=req.mentor.user_id,
        startup_id=req.startup.user_id,
        date=datetime.combine(req.request_date, req.request_time),
        status=random.choice(['Pending', 'Completed', 'Cancelled'])
    )
    db.session.add(session)

db.session.commit()

print("✅ Seeding complete: mentorship requests and sessions created.")

