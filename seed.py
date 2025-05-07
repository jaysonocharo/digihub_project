from app import create_app, db
from app.models import User, Startup, Investor
from app.matching import match_startups_to_investors
from faker import Faker
from random import choice, randint, uniform
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash

app = create_app()
bcrypt = Bcrypt(app)
faker = Faker()

with app.app_context():
    #
    # db.drop_all()
    db.create_all()

    # Optional Admin
    # admin = User(
    #     username='admin',
    #     email='admin@digihub.co.ke',
    #     password=generate_password_hash('admin123'),
    #     role='admin',
    #     approved=True
    # )
    # db.session.add(admin)

    industries = ["Fintech", "Healthtech", "Edtech", "AgriTech"]
    stages = ["seed", "pre-seed", "series-a"]
    tech_stacks = {
        "Fintech": "Python, Django, PostgreSQL",
        "Healthtech": "Node.js, Express, MongoDB",
        "Edtech": "Java, Spring Boot, MySQL",
        "AgriTech": "Flask, Vue.js, SQLite"
    }

    def generate_entities(match_quality):
        category = choice(industries)
        stage = choice(stages)
        tech_stack = tech_stacks[category]

        if match_quality == "high":
            thesis = f"Our firm backs {category.lower()} startups using {tech_stack}. We focus on {tech_stack}."
            startup_stack = f"{tech_stack}. We are a {category.lower()} company using {tech_stack} technologies."
        elif match_quality == "medium":
            thesis = f"We support innovation in {category.lower()} with modern stacks like {tech_stack.split(',')[0]}"
            startup_stack = f"We're using {tech_stack.split(',')[1]} for our {category.lower()} platform."
        elif match_quality == "low":
            thesis = f"Focused on scalable solutions. Interested in SaaS and automation tools."
            startup_stack = "Using GoLang, Redis, and Kubernetes."
        else:  # very low
            thesis = "We invest in logistics and real estate ventures using COBOL and Oracle."
            startup_stack = "Built with Flutter and Firebase. Targeting education sector."

        # Investor
        inv_user = User(
            username=faker.user_name(),
            email=faker.unique.email(),
            password=bcrypt.generate_password_hash("test1234").decode('utf-8'),
            role="investor",
            approved=True
        )
        db.session.add(inv_user)
        db.session.flush()

        investor = Investor(
            user_id=inv_user.id,
            firm_name=faker.company(),
            location=faker.city(),
            check_size_min=1000000,
            check_size_max=5000000,
            industry_focus=category if match_quality != "very low" else "Logistics",
            stage_focus=stage,
            portfolio=faker.sentence(),
            deal_preferences="Equity",
            investment_thesis=thesis,
            engagement_style="hands-on",
            past_exits="Exited startups in 2020 and 2022"
        )
        db.session.add(investor)

        # Startup
        st_user = User(
            username=faker.user_name(),
            email=faker.unique.email(),
            password=bcrypt.generate_password_hash("test1234").decode('utf-8'),
            role="startup",
            approved=True
        )
        db.session.add(st_user)
        db.session.flush()

        startup = Startup(
            user_id=st_user.id,
            company_name=faker.company(),
            industry=category if match_quality != "very low" else "Edtech",
            location=faker.city(),
            founding_date=faker.date_between(start_date='-3y', end_date='today'),
            team_size=randint(3, 15),
            revenue_streams=faker.text(),
            pricing_strategy=faker.sentence(),
            customer_acquisition_cost=uniform(100.0, 1000.0),
            stage=stage,
            funding_needed=randint(1500000, 4000000),
            valuation=randint(5000000, 10000000),
            previous_funding="Seed round",
            revenue=randint(100000, 1000000),
            mrr=randint(10000, 100000),
            user_growth=uniform(10.0, 30.0),
            partnerships="Partnered with industry leaders",
            tech_stack=startup_stack,
            ip_rights="Patent Pending",
            competitive_advantage="Strong team and early traction",
            tam=uniform(1e6, 5e7),
            sam=uniform(5e5, 1e7),
            competition="Other players include ABC, XYZ",
            website="https://example.com",
            social_links="https://linkedin.com/company/example"
        )
        db.session.add(startup)

    # Seed different match qualities
    for _ in range(3):
        generate_entities("high")
    for _ in range(3):
        generate_entities("medium")
    for _ in range(2):
        generate_entities("low")
    for _ in range(2):
        generate_entities("very low")

    db.session.commit()
    print("✅ Seeded data with varied match quality.")

    # Run matching logic and print results
    matches = match_startups_to_investors()
    for match in matches:
        print(f"{match['tier']} | {match['startup'].company_name} ↔ {match['investor'].firm_name} | Score: {match['score']}%")
