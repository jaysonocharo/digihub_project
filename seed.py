from app import create_app, db
from app.models import User

app = create_app()
app.app_context().push()

bios_by_id = {
    4: "We are revolutionizing patient diagnostics with mobile labs and AI-assisted triage tools for rural clinics.",
    5: "We design gamified e-learning platforms to keep students engaged, even in low-resource environments.",
    6: "Our platform empowers farmers with weather insights and smart crop planning tools.",
    7: "We connect smallholder farmers directly to buyers using blockchain to ensure fair pricing.",
    8: "We develop wearable health monitors to track vitals in real-time and share them with care providers.",
    9: "We offer micro-investment opportunities through mobile wallets to increase financial inclusion.",
    10: "We're using drone tech to monitor soil health and optimize yields for medium-scale farms.",
    11: "Our telemedicine platform brings affordable specialist care to underserved urban zones.",
    12: "We simplify SME lending through AI-based risk profiling and a seamless mobile application process.",
    45: "Perfect_startup is building Kenya’s first decentralized finance platform focused on youth-led businesses.",
    46: "We develop AI tools for recycling management and carbon tracking for urban cities.",
    47: "We help rural farmers switch to sustainable irrigation and provide real-time pest alerts via SMS.",
    3: "Our e-commerce site specializes in made-in-Africa fashion, shipped nationwide within 48 hours.",
    48: "We're improving maternal healthcare access by combining community health workers with mobile tools.",
    41: "Our hybrid solar battery packs bring power to remote schools and clinics off the national grid.",
    42: "We offer precision agriculture tech bundled with agribusiness mentorship for rural cooperatives.",
    49: "We’re creating payment APIs for Africa’s informal sector, starting with local merchants.",
    54: "We build AI models that localize content recommendations for regional media streaming platforms.",
    55: "Our fintech tools help first-time investors manage risk and automate savings goals.",
    56: "We digitize inventory and customer loyalty programs for small retail shops in emerging markets.",
}

# Update bios
for user_id, bio_text in bios_by_id.items():
    user = User.query.get(user_id)
    if user:
        user.bio = bio_text
        print(f"Updated bio for user ID {user_id}")
    else:
        print(f"User ID {user_id} not found.")

# Commit changes
db.session.commit()
print("All specified bios updated.")













# # #  UPDATED BIOS FOR REALSTARTUPS 1-10  ###
# from app import create_app, db
# from app.models import User

# app = create_app()

# def update_startup_bios():
#     with app.app_context():
#         # Map of usernames to their new bios
#         bio_updates = {
#             "realstartup1": "M-KOPA provides affordable solar energy systems and smartphone financing to off-grid communities through flexible pay-as-you-go mobile payments. Our IoT-enabled solutions have empowered over 1 million homes across Africa with clean energy and digital connectivity.",
#             "realstartup2": "Wasoko is revolutionizing African retail by digitizing the supply chain for informal shops. Our platform offers just-in-time delivery of FMCG goods with embedded financing, helping over 50,000 retailers optimize inventory and grow their businesses.",
#             "realstartup3": "Twiga connects smallholder farmers directly to urban retailers through our tech-driven food distribution platform. We reduce post-harvest losses by 30% while ensuring fair prices for farmers and fresh produce for vendors across Kenya.",
#             "realstartup4": "MoKo designs and manufactures high-quality, affordable furniture for African homes. By cutting out middlemen and offering flexible payment plans, we make stylish home furnishings accessible to Kenya's growing middle class.",
#             "realstartup5": "SunCulture's solar-powered irrigation systems help smallholder farmers increase yields by 300%. Our bundled solutions combine solar tech, drip irrigation, and pay-as-you-go financing to combat climate change impacts on agriculture.",
#             "realstartup6": "Apollo uses AI and satellite data to provide smallholder farmers with customized agronomic advice, quality inputs, and credit. Our technology helps farmers optimize their operations and double their productivity.",
#             "realstartup7": "KOKO operates Africa's largest network of bioethanol fuel ATMs, providing clean cooking solutions to urban households. Our smart cookstoves and fuel distribution system reduce indoor air pollution while saving families money.",
#             "realstartup8": "Sendy's tech platform connects businesses to vetted delivery providers across East Africa. We simplify logistics with real-time tracking, transparent pricing, and API integrations for e-commerce platforms.",
#             "realstartup9": "Lami is building Africa's digital insurance infrastructure. Our API-first platform enables any business to easily create, distribute, and manage insurance products tailored to their customers' needs.",
#             "realstartup10": "Pezesha provides embedded finance solutions for Africa's underserved SMEs. Our credit scoring platform connects small businesses to affordable working capital through partnerships with financial institutions."
#         }

#         success_count = 0
#         for username, new_bio in bio_updates.items():
#             user = User.query.filter_by(username=username).first()
#             if user:
#                 user.bio = new_bio
#                 print(f"✓ Updated bio for {username}")
#                 success_count += 1
#             else:
#                 print(f"✗ User {username} not found, skipping")

#         try:
#             db.session.commit()
#             print(f"\n✅ Successfully updated {success_count}/10 bios")
#             print("Changes committed to database.")
#         except Exception as e:
#             db.session.rollback()
#             print(f"\n❌ Error updating bios: {str(e)}")
#             print("Changes rolled back.")

# if __name__ == "__main__":
#     update_startup_bios()







 ####  SEEDED 10 REALISTIC STARTUPS ###

# from app import create_app, db, bcrypt
# from app.models import User, Startup, Investor
# from datetime import datetime
# import random

# app = create_app()

# def create_user(username, email, password, role):
#     if not User.query.filter_by(email=email).first():
#         user = User(
#             username=username,
#             email=email,
#             password=bcrypt.generate_password_hash(password).decode('utf-8'),
#             role=role,
#             approved=True
#         )
#         db.session.add(user)
#         db.session.commit()
#         return user
#     return None

# def seed_real_investors():
#     investors = [
#         {
#             "username": "realinvestor1",
#             "email": "real_investor1@test.com",
#             "firm_name": "TLcom Capital",
#             "location": "Nairobi",
#             "check_size_min": 100000,
#             "check_size_max": 2000000,
#             "industry_focus": "FinTech",
#             "stage_focus": "Pre-Series A, Series A, Series B",
#             "investment_thesis": "We invest in high-growth African startups with scalable tech platforms in finance, education, and logistics.",
#             "deal_preferences": "Equity",
#             "portfolio": "Andela, Twiga Foods, uLesson",
#             "engagement_style": "Hands-on",
#             "past_exits": "Andela (partial exit)"
#         },
#         {
#             "username": "realinvestor2",
#             "email": "real_investor2@test.com",
#             "firm_name": "Novastar Ventures",
#             "location": "Nairobi",
#             "check_size_min": 50000,
#             "check_size_max": 1000000,
#             "industry_focus": "Clean Energy",
#             "stage_focus": "Seed, Series A",
#             "investment_thesis": "Backing mission-driven businesses that address basic needs in East Africa sustainably.",
#             "deal_preferences": "Equity",
#             "portfolio": "MoKo, M-KOPA, Sanergy",
#             "engagement_style": "Supportive",
#             "past_exits": "None disclosed"
#         },
#         {
#             "username": "realinvestor3",
#             "email": "real_investor3@test.com",
#             "firm_name": "Partech Africa",
#             "location": "Dakar / Nairobi",
#             "check_size_min": 200000,
#             "check_size_max": 5000000,
#             "industry_focus": "E-commerce & Retail",
#             "stage_focus": "Series A, Series B",
#             "investment_thesis": "We scale digital platforms reshaping retail, distribution, and logistics across the continent.",
#             "deal_preferences": "Equity",
#             "portfolio": "Yoco, TradeDepot, Wave",
#             "engagement_style": "Board-level strategy",
#             "past_exits": "2 undisclosed"
#         },
#         {
#             "username": "realinvestor4",
#             "email": "real_investor4@test.com",
#             "firm_name": "Shell Foundation",
#             "location": "London / Nairobi",
#             "check_size_min": 30000,
#             "check_size_max": 300000,
#             "industry_focus": "AgTech, CleanTech",
#             "stage_focus": "Seed, Series A",
#             "investment_thesis": "We support inclusive innovation improving energy access and agricultural livelihoods.",
#             "deal_preferences": "Grants, Equity",
#             "portfolio": "SunCulture, BURN, BioLite",
#             "engagement_style": "Impact-driven",
#             "past_exits": "-"
#         },
#         {
#             "username": "realinvestor5",
#             "email": "real_investor5@test.com",
#             "firm_name": "Anthemis Group",
#             "location": "London",
#             "check_size_min": 250000,
#             "check_size_max": 2000000,
#             "industry_focus": "FinTech, InsurTech",
#             "stage_focus": "Series A, Series B",
#             "investment_thesis": "Building the future of embedded finance by investing in agile and inclusive platforms.",
#             "deal_preferences": "Equity",
#             "portfolio": "Apollo Agriculture, Trov, Better",
#             "engagement_style": "Product advisory",
#             "past_exits": "2 successful IPOs"
#         }
#     ]

#     for inv in investors:
#         user = create_user(inv["username"], inv["email"], "password123", "investor")
#         if user:
#             investor = Investor(
#                 user_id=user.id,
#                 firm_name=inv["firm_name"],
#                 location=inv["location"],
#                 check_size_min=inv["check_size_min"],
#                 check_size_max=inv["check_size_max"],
#                 industry_focus=inv["industry_focus"],
#                 stage_focus=inv["stage_focus"],
#                 investment_thesis=inv["investment_thesis"],
#                 deal_preferences=inv["deal_preferences"],
#                 portfolio=inv["portfolio"],
#                 engagement_style=inv["engagement_style"],
#                 past_exits=inv["past_exits"]
#             )
#             db.session.add(investor)

# def run():
#     with app.app_context():
#         seed_real_investors()
#         db.session.commit()
#         print("✅ 5 real Kenyan investors seeded.")

# if __name__ == "__main__":
#     run()












####  SEEDED 10 REALISTIC STARTUPS ###

# from app import create_app, db
# from app.models import User, Startup, Investor
# from faker import Faker
# import random
# from datetime import datetime

# fake = Faker()
# app = create_app()

# def seed_startups_and_investors():
#     with app.app_context():

#         # Startup 1
#         user = User(
#             username="realstartup1",
#             email="realstartup1@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/m-kopa",
#             contact_info="+254700000001"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="M-KOPA",
#             logo="static/uploads/logo_1.png",
#             industry="Clean Energy",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Pay-as-you-go solar energy systems and smartphone financing",
#             pricing_strategy="Flexible installment payments over mobile money",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Series C",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Series C funding from CDC Group",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Safaricom, Mastercard",
#             tech_stack="IoT, mobile payments, data analytics",
#             ip_rights="Proprietary solar metering platform",
#             competitive_advantage="Affordable financing for low-income customers in off-grid areas",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_1.pdf",
#             demo_video="static/uploads/demo_1.mp4",
#             website="https://m-kopa.com",
#             social_links="https://linkedin.com/company/m-kopa",
#             phone_number="+254700000001",
#             whatsapp="+254700000001",
#             instagram="https://instagram.com/mkopa_ke",
#             facebook="https://facebook.com/mkopa",
#             twitter_x="https://twitter.com/mkopa",
#             linkedin="https://linkedin.com/company/m-kopa"
#         )
#         db.session.add(startup)


#         # Startup 2
#         user = User(
#             username="realstartup2",
#             email="realstartup2@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/wasoko",
#             contact_info="+254700000002"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="Wasoko",
#             logo="static/uploads/logo_2.png",
#             industry="E-commerce & Retail",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Distribution margin on FMCG products",
#             pricing_strategy="Bulk discounts to retailers",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Series B",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Series B led by Tiger Global",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Unilever, P&G",
#             tech_stack="Logistics software, mobile CRM",
#             ip_rights="Proprietary supply chain technology",
#             competitive_advantage="Just-in-time delivery and credit for small retailers",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_2.pdf",
#             demo_video="static/uploads/demo_2.mp4",
#             website="https://wasoko.com",
#             social_links="https://linkedin.com/company/wasoko",
#             phone_number="+254700000002",
#             whatsapp="+254700000002",
#             instagram="https://instagram.com/wasoko_africa",
#             facebook="https://facebook.com/wasokoafrica",
#             twitter_x="https://twitter.com/wasoko_africa",
#             linkedin="https://linkedin.com/company/wasoko"
#         )
#         db.session.add(startup)


#         # Startup 3
#         user = User(
#             username="realstartup3",
#             email="realstartup3@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/twiga-foods",
#             contact_info="+254700000003"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="Twiga Foods",
#             logo="static/uploads/logo_3.png",
#             industry="Foodtech",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Wholesale supply chain services for fresh produce",
#             pricing_strategy="Dynamic pricing based on market data",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Series C",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Series C from Goldman Sachs",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="IFC, Microsoft",
#             tech_stack="ERP systems, route optimization",
#             ip_rights="Supply chain automation tools",
#             competitive_advantage="Farm-to-market logistics reducing post-harvest losses",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_3.pdf",
#             demo_video="static/uploads/demo_3.mp4",
#             website="https://twiga.com",
#             social_links="https://linkedin.com/company/twiga-foods",
#             phone_number="+254700000003",
#             whatsapp="+254700000003",
#             instagram="https://instagram.com/twigafoods",
#             facebook="https://facebook.com/twigafoods",
#             twitter_x="https://twitter.com/twigafoods",
#             linkedin="https://linkedin.com/company/twiga-foods"
#         )
#         db.session.add(startup)


#         # Startup 4
#         user = User(
#             username="realstartup4",
#             email="realstartup4@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/moko-home-living",
#             contact_info="+254700000004"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="MoKo Home + Living",
#             logo="static/uploads/logo_4.png",
#             industry="E-commerce & Retail",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Online furniture and home decor sales",
#             pricing_strategy="Affordable installments and factory-direct pricing",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Seed",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Seed funding from Novastar Ventures",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Safaricom, Sendy",
#             tech_stack="E-commerce, supply chain ERP",
#             ip_rights="Trademarked designs and patterns",
#             competitive_advantage="Local manufacturing and branding",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_4.pdf",
#             demo_video="static/uploads/demo_4.mp4",
#             website="https://moko.co.ke",
#             social_links="https://linkedin.com/company/moko-home-living",
#             phone_number="+254700000004",
#             whatsapp="+254700000004",
#             instagram="https://instagram.com/moko_kenya",
#             facebook="https://facebook.com/mokohome",
#             twitter_x="https://twitter.com/moko_ke",
#             linkedin="https://linkedin.com/company/moko-home-living"
#         )
#         db.session.add(startup)


#         # Startup 5
#         user = User(
#             username="realstartup5",
#             email="realstartup5@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/sunculture",
#             contact_info="+254700000005"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="SunCulture",
#             logo="static/uploads/logo_5.png",
#             industry="AgTech",
#             location="Kiambu",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Solar irrigation kits, bundled with financing",
#             pricing_strategy="Prepaid kits and pay-as-you-go models",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Series A",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Grants from Shell Foundation",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Equity Bank, Syngenta",
#             tech_stack="Solar hardware, mobile control apps",
#             ip_rights="Patented irrigation kits",
#             competitive_advantage="First solar-powered irrigation tech in Kenya",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_5.pdf",
#             demo_video="static/uploads/demo_5.mp4",
#             website="https://sunculture.com",
#             social_links="https://linkedin.com/company/sunculture",
#             phone_number="+254700000005",
#             whatsapp="+254700000005",
#             instagram="https://instagram.com/sunculture",
#             facebook="https://facebook.com/sunculture",
#             twitter_x="https://twitter.com/sunculture",
#             linkedin="https://linkedin.com/company/sunculture"
#         )
#         db.session.add(startup)


#         # Startup 6
#         user = User(
#             username="realstartup6",
#             email="realstartup6@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/apollo-agriculture",
#             contact_info="+254700000006"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="Apollo Agriculture",
#             logo="static/uploads/logo_6.png",
#             industry="AgTech / FinTech",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Sales of farm inputs, insurance premiums, and interest from credit facilities.",
#             pricing_strategy="Bundled packages with flexible repayment plans.",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Series A",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Raised $6 million in Series A funding led by Anthemis.",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Collaborations with local agro-dealers and financial institutions.",
#             tech_stack="Machine learning, mobile applications, satellite imagery.",
#             ip_rights="Proprietary algorithms for credit scoring and agronomic recommendations.",
#             competitive_advantage="Utilizes AI and satellite data to optimize farming decisions for smallholder farmers.",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_6.pdf",
#             demo_video="static/uploads/demo_6.mp4",
#             website="https://www.apolloagriculture.com/",
#             social_links="https://linkedin.com/company/apollo-agriculture",
#             phone_number="+254700000006",
#             whatsapp="+254700000006",
#             instagram="https://instagram.com/apolloagriculture",
#             facebook="https://facebook.com/apolloagriculture",
#             twitter_x="https://twitter.com/ApolloAgri",
#             linkedin="https://linkedin.com/company/apollo-agriculture"
#         )
#         db.session.add(startup)


#         # Startup 7
#         user = User(
#             username="realstartup7",
#             email="realstartup7@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/koko-networks",
#             contact_info="+254700000007"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="KOKO Networks",
#             logo="static/uploads/logo_7.png",
#             industry="CleanTech / Energy",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Sale of bioethanol fuel, smart cookstoves, and carbon credits.",
#             pricing_strategy="Affordable pricing for low-income households with pay-as-you-go options.",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Growth Stage",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Secured over $100 million through carbon credit sales and partnerships.",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Collaborations with Vivo Energy and Rand Merchant Bank.",
#             tech_stack="IoT-enabled fuel dispensers, cloud-based monitoring systems.",
#             ip_rights="Patented fuel distribution technology.",
#             competitive_advantage="Extensive network of fuel ATMs and integration with local retail outlets.",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_7.pdf",
#             demo_video="static/uploads/demo_7.mp4",
#             website="https://kokonetworks.com/",
#             social_links="https://linkedin.com/company/koko-networks",
#             phone_number="+254700000007",
#             whatsapp="+254700000007",
#             instagram="https://instagram.com/kokonetworks",
#             facebook="https://facebook.com/kokonetworks",
#             twitter_x="https://twitter.com/kokonetworks",
#             linkedin="https://linkedin.com/company/koko-networks"
#         )
#         db.session.add(startup)


#         # Startup 8
#         user = User(
#             username="realstartup8",
#             email="realstartup8@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/sendy",
#             contact_info="+254700000008"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="Sendy",
#             logo="static/uploads/logo_8.png",
#             industry="Logistics / E-commerce",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Delivery fees, subscription services for businesses.",
#             pricing_strategy="Transparent pricing with real-time tracking.",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Series B",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Raised $20 million in Series B funding led by Atlantica Ventures.",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Collaborations with e-commerce platforms and retailers.",
#             tech_stack="Mobile and web applications, API integrations.",
#             ip_rights="Proprietary logistics management platform.",
#             competitive_advantage="Seamless integration for businesses to manage deliveries and logistics.",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_8.pdf",
#             demo_video="static/uploads/demo_8.mp4",
#             website="https://www.sendyit.com/",
#             social_links="https://linkedin.com/company/sendy",
#             phone_number="+254700000008",
#             whatsapp="+254700000008",
#             instagram="https://instagram.com/sendykenya",
#             facebook="https://facebook.com/sendykenya",
#             twitter_x="https://twitter.com/SendyKenya",
#             linkedin="https://linkedin.com/company/sendy"
#         )
#         db.session.add(startup)


#         # Startup 9
#         user = User(
#             username="realstartup9",
#             email="realstartup9@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/lamiworld",
#             contact_info="+254700000009"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="Lami Technologies",
#             logo="static/uploads/logo_9.png",
#             industry="InsurTech",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="API integrations for insurance distribution, commissions from policy sales.",
#             pricing_strategy="Competitive pricing with customizable insurance products.",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Seed",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Raised $3.7 million in seed extension funding led by Harlem Capital.",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Collaborations with insurance companies and digital platforms.",
#             tech_stack="RESTful APIs, cloud-based platforms.",
#             ip_rights="Proprietary insurance distribution technology.",
#             competitive_advantage="End-to-end digital insurance platform enabling easy policy creation and management.",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_9.pdf",
#             demo_video="static/uploads/demo_9.mp4",
#             website="https://www.lami.world/",
#             social_links="https://linkedin.com/company/lamiworld",
#             phone_number="+254700000009",
#             whatsapp="+254700000009",
#             instagram="https://instagram.com/lamiinsurtech",
#             facebook="https://facebook.com/lamiinsurtech",
#             twitter_x="https://twitter.com/LamiInsurtech",
#             linkedin="https://linkedin.com/company/lamiworld"
#         )
#         db.session.add(startup)


#         # Startup 10
#         user = User(
#             username="realstartup10",
#             email="realstartup10@test.com",
#             password="$2b$12$T3Zhw6Z2mSxzuhRgPfHOreCkZnMiUwSc7wRye3WaVgl/NHczAmq4q",
#             role="startup",
#             approved=True,
#             bio=fake.text(),
#             linkedin_profile="https://linkedin.com/company/pezesha",
#             contact_info="+254700000010"
#         )
#         db.session.add(user)
#         db.session.flush()
#         startup = Startup(
#             user_id=user.id,
#             company_name="Pezesha",
#             logo="static/uploads/logo_10.png",
#             industry="FinTech",
#             location="Nairobi",
#             founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#             team_size=random.randint(5, 30),
#             revenue_streams="Interest from microloans, fees from financial services.",
#             pricing_strategy="Affordable interest rates tailored for SMEs.",
#             customer_acquisition_cost=random.uniform(10, 150),
#             stage="Pre-Series A",
#             funding_needed=random.uniform(50000, 250000),
#             valuation=random.uniform(500000, 4000000),
#             previous_funding="Announced $11 million in Pre-Series A funding.",
#             revenue=random.uniform(10000, 250000),
#             mrr=random.uniform(1000, 50000),
#             user_growth=random.uniform(5, 50),
#             partnerships="Collaborations with financial institutions and digital platforms.",
#             tech_stack="Credit scoring algorithms, mobile platforms.",
#             ip_rights="Proprietary digital lending infrastructure.",
#             competitive_advantage="Embedded finance infrastructure providing access to credit for underserved SMEs.",
#             tam=random.uniform(1e6, 1e8),
#             sam=random.uniform(1e5, 1e7),
#             competition=fake.company(),
#             pitch_deck="static/uploads/pitch_10.pdf",
#             demo_video="static/uploads/demo_10.mp4",
#             website="https://pezesha.com/",
#             social_links="https://linkedin.com/company/pezesha",
#             phone_number="+254700000010",
#             whatsapp="+254700000010",
#             instagram="https://instagram.com/pezesha",
#             facebook="https://facebook.com/pezesha",
#             twitter_x="https://twitter.com/Pezesha",
#             linkedin="https://linkedin.com/company/pezesha"
#         )
#         db.session.add(startup)

#         db.session.commit()
#         print('✅ 10 real Kenyan startups seeded.')
        
#         db.session.commit()
#         print("✅ Database seeded successfully!")


# if __name__ == '__main__':
#     seed_startups_and_investors()




# from app import create_app, db, bcrypt
# from app.models import User, Startup, Investor
# from datetime import datetime

# app = create_app()

# def create_user(username, email, password, role):
#     if not User.query.filter_by(email=email).first():
#         user = User(
#             username=username,
#             email=email,
#             password=bcrypt.generate_password_hash(password).decode('utf-8'),
#             role=role,
#             approved=True
#         )
#         db.session.add(user)
#         db.session.commit()
#         return user
#     return None

# def seed_additional_startups():
#     data = [
#         {
#             'username': 'buzzwords_ai',
#             'email': 'buzzwords_ai@example.com',
#             'company': 'AI Synergy Labs',
#             'industry': 'Technology',
#             'funding': 750000,
#             'stage': 'Series B',
#             'tech_stack': 'AI, Blockchain, IoT',
#             'advantage': 'Disruptive synergy via innovative paradigms'
#         },
#         {
#             'username': 'empty_fields',
#             'email': 'empty_fields@example.com',
#             'company': 'Zero Info Inc.',
#             'industry': 'Finance',
#             'funding': 100000,
#             'stage': 'Seed',
#             'tech_stack': '',
#             'advantage': ''
#         },
#         {
#             'username': 'stage_only',
#             'email': 'stage_only@example.com',
#             'company': 'ScaleMeUp',
#             'industry': 'Retail',
#             'funding': 200000,
#             'stage': 'Series A',
#             'tech_stack': 'Flask, PostgreSQL',
#             'advantage': 'Operational scaling framework'
#         }
#     ]

#     for item in data:
#         user = create_user(item['username'], item['email'], 'password123', 'startup')
#         if user:
#             startup = Startup(
#                 user_id=user.id,
#                 company_name=item['company'],
#                 industry=item['industry'],
#                 funding_needed=item['funding'],
#                 stage=item['stage'],
#                 tech_stack=item['tech_stack'],
#                 competitive_advantage=item['advantage'],
#                 revenue_streams="Freemium, B2B2C",
#                 pricing_strategy="Usage-based",
#                 founding_date=datetime(2022, 6, 1)
#             )
#             db.session.add(startup)

# def seed_additional_investors():
#     data = [
#         {
#             'username': 'buzzwords_fund',
#             'email': 'buzzwords_fund@example.com',
#             'firm': 'Synergy VC',
#             'industry': 'Technology',
#             'min': 500000,
#             'max': 1000000,
#             'stage': 'Series B',
#             'thesis': 'Empowering synergy through disruption',
#             'portfolio': 'InnoCorp, DeepNext'
#         },
#         {
#             'username': 'generic_investor',
#             'email': 'generic_investor@example.com',
#             'firm': 'Blank Slate Capital',
#             'industry': 'Finance',
#             'min': 50000,
#             'max': 200000,
#             'stage': 'Seed, Series A',
#             'thesis': '',
#             'portfolio': ''
#         }
#     ]

#     for item in data:
#         user = create_user(item['username'], item['email'], 'password123', 'investor')
#         if user:
#             investor = Investor(
#                 user_id=user.id,
#                 firm_name=item['firm'],
#                 industry_focus=item['industry'],
#                 check_size_min=item['min'],
#                 check_size_max=item['max'],
#                 stage_focus=item['stage'],
#                 investment_thesis=item['thesis'],
#                 portfolio=item['portfolio'],
#                 engagement_style="Hybrid"
#             )
#             db.session.add(investor)

# def run():
#     with app.app_context():
#         seed_additional_startups()
#         seed_additional_investors()
#         db.session.commit()
#         print("✅ All startups and investors seeded (including edge cases and extended test set).")

# if __name__ == "__main__":
#     run()




####  SEEDED 2 PAIRS OF MATCHING STARTUPS AND INVESTORS

# import os
# from app import create_app, db, bcrypt
# from app.models import User, Startup, Investor
# from werkzeug.security import generate_password_hash
# from datetime import datetime

# app = create_app()

# def create_user(username, email, password, role):
#     if not User.query.filter_by(email=email).first():
#         user = User(
#             username=username,
#             email=email,
#             password=bcrypt.generate_password_hash(password).decode('utf-8'),
#             role=role,
#             approved=True
#         )
#         db.session.add(user)
#         db.session.commit()
#         return user
#     return None

# def seed_startups():
#     startup_user = create_user("match_startup1", "match_startup1@example.com", "password123", "startup")
#     if startup_user:
#         startup = Startup(
#             user_id=startup_user.id,
#             company_name="GreenTech AI",
#             industry="Energy",
#             location="Nairobi",
#             founding_date=datetime(2022, 1, 15),
#             team_size=10,
#             tech_stack="Python, TensorFlow, React",
#             competitive_advantage="Proprietary energy consumption prediction model",
#             pricing_strategy="Tiered SaaS",
#             revenue_streams="Subscriptions, Licensing",
#             funding_needed=300000.0,
#             valuation=1500000.0,
#             stage="Seed"
#         )
#         db.session.add(startup)

#     startup_user2 = create_user("match_startup2", "match_startup2@example.com", "password123", "startup")
#     if startup_user2:
#         startup = Startup(
#             user_id=startup_user2.id,
#             company_name="AgroTrack",
#             industry="Agriculture",
#             location="Kisumu",
#             founding_date=datetime(2021, 6, 20),
#             team_size=8,
#             tech_stack="Django, Vue.js, PostgreSQL",
#             competitive_advantage="Real-time soil monitoring",
#             pricing_strategy="Freemium with paid analytics",
#             revenue_streams="Hardware sales, SaaS analytics",
#             funding_needed=500000.0,
#             valuation=2500000.0,
#             stage="Series A"
#         )
#         db.session.add(startup)

# def seed_investors():
#     investor_user = create_user("match_investor1", "match_investor1@example.com", "password123", "investor")
#     if investor_user:
#         investor = Investor(
#             user_id=investor_user.id,
#             firm_name="Green Future Capital",
#             location="Nairobi",
#             check_size_min=100000.0,
#             check_size_max=500000.0,
#             industry_focus="Energy",
#             stage_focus="Seed, Series A",
#             investment_thesis="We fund sustainable tech for Africa.",
#             engagement_style="Hands-on",
#             portfolio="SolarPlus, EcoGen"
#         )
#         db.session.add(investor)

#     investor_user2 = create_user("match_investor2", "match_investor2@example.com", "password123", "investor")
#     if investor_user2:
#         investor = Investor(
#             user_id=investor_user2.id,
#             firm_name="AgriFund Ventures",
#             location="Nakuru",
#             check_size_min=300000.0,
#             check_size_max=1000000.0,
#             industry_focus="Agriculture",
#             stage_focus="Series A",
#             investment_thesis="Precision agriculture is the future.",
#             engagement_style="Passive",
#             portfolio="FarmTech, SoilSmart"
#         )
#         db.session.add(investor)

# def run():
#     with app.app_context():
#         seed_startups()
#         seed_investors()
#         db.session.commit()
#         print("✅ Test startups and investors added successfully.")

# if __name__ == "__main__":
#     run()














#####  TRIED TO SEED REALISTIC 5 STARTUPS AND 5 INVESTORS  ####

# import os
# import random
# from faker import Faker
# from datetime import datetime, timedelta
# from app import create_app, db
# from app.models import User, Startup, Investor, Mentor
# import bcrypt

# # Setup
# app = create_app()
# fake = Faker()
# app.app_context().push()


# # Global password
# password = 'test123'
# hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# # Media placeholders
# DEFAULT_LOGO = "uploads/logos/default.png"
# DEFAULT_PITCH = "uploads/pitch_decks/default.pdf"
# DEFAULT_VIDEO = "uploads/demo_videos/default.mp4"

# # ----------- 5 Startups -----------

# startups = [
#     {
#         "username": "agrosoko",
#         "email": "info@agrosoko.co.ke",
#         "company_name": "Agrosoko",
#         "location": "Eldoret",
#         "industry": "AgriTech",
#         "stage": "Seed",

#         "tech_stack": "Flutter, Firebase",
#         "competitive_advantage": "Real-time produce demand forecasting and logistics partnerships.",
#         "pricing_strategy": "Freemium model with commission on sales.",
#         "valuation": 6000000,
#         "funding_needed": 1500000,
#     },
#     {
#         "username": "clinicpal",
#         "email": "founder@clinicpal.ke",
#         "company_name": "ClinicPal",
#         "location": "Nairobi",
#         "industry": "HealthTech",
#         "stage": "Series A",

#         "tech_stack": "React Native, Django",
#         "competitive_advantage": "Offline syncing and local language UI.",
#         "pricing_strategy": "SaaS monthly plans with NGO discounts.",
#         "valuation": 20000000,
#         "funding_needed": 5000000,
#     },
#     {
#         "username": "tujengane",
#         "email": "hello@tujengane.org",
#         "company_name": "Tujengane",
#         "location": "Kisumu",
#         "industry": "CivicTech",
#         "stage": "Pre-Seed",

#         "tech_stack": "Vue.js, Firebase",
#         "competitive_advantage": "Gamified civic challenges and policy bot.",
#         "pricing_strategy": "Free with grant support and freemium NGO tools.",
#         "valuation": 2000000,
#         "funding_needed": 800000,
#     },
#     {
#         "username": "learnkazi",
#         "email": "admin@learnkazi.com",
#         "company_name": "LearnKazi",
#         "location": "Mombasa",
#         "industry": "EdTech",
#         "stage": "Seed",

#         "tech_stack": "Laravel, MySQL",
#         "competitive_advantage": "Co-designed with local employers and success-based pricing.",
#         "pricing_strategy": "Pay-per-skill and sponsorships.",
#         "valuation": 5000000,
#         "funding_needed": 1200000,
#     },
#     {
#         "username": "swiftbeba",
#         "email": "founders@swiftbeba.co.ke",
#         "company_name": "SwiftBeba",
#         "location": "Nakuru",
#         "industry": "Mobility",
#         "stage": "Series A",

#         "tech_stack": "Node.js, MongoDB",
#         "competitive_advantage": "Real-time traffic rerouting and loyalty program.",
#         "pricing_strategy": "10% service fee + B2B transport analytics.",
#         "valuation": 25000000,
#         "funding_needed": 7000000,
#     },
# ]


# for s in startups:
#     if User.query.filter((User.username == s['username']) | (User.email == s['email'])).first():
#         print(f"⚠️ Skipping duplicate startup user: {s['username']}")
#         continue
#     print(f"✅ Adding Startup: {s['company_name']}")
#     user = User(username=s['username'], email=s['email'], password=hashed_pw, role='startup')
#     db.session.add(user)
#     db.session.flush()
#     startup = Startup(
#         user_id=user.id,
#         company_name=s['company_name'],
#         location=s['location'],
#         industry=s['industry'],

#         tech_stack=s['tech_stack'],
#         competitive_advantage=s['competitive_advantage'],
#         pricing_strategy=s['pricing_strategy'],
#         valuation=s['valuation'],
#         funding_needed=s['funding_needed'],
#         logo=DEFAULT_LOGO,
#         pitch_deck=DEFAULT_PITCH,
#         demo_video=DEFAULT_VIDEO,
#     )
#     db.session.add(startup)

# # ----------- 5 Investors -----------

# investors = [
#     {
#         "username": "africafund",
#         "email": "dealflow@africafund.ke",
#         "firm_name": "AfricaFund Ventures",
#         "location": "Nairobi",
#         "check_size_min": 100000,
#         "check_size_max": 1000000,
#         "investment_focus": "FinTech, AgriTech, Mobility",
#         "portfolio": "M-Kopa, Twiga, Sendy",
#         "deal_preferences": "Series A and above, revenue-generating companies.",
#         "investment_thesis": "Backing proven African business models with a digital edge.",
#         "engagement_style": "Hands-on with quarterly reviews.",
#         "past_exits": "Cellulant, iProcure",
#     },
#     {
#         "username": "masharikiangel",
#         "email": "invest@masharikiangels.co.ke",
#         "firm_name": "Mashariki Angels",
#         "location": "Mombasa",
#         "check_size_min": 20000,
#         "check_size_max": 250000,
#         "investment_focus": "HealthTech, EdTech, CivicTech",
#         "portfolio": "Ilara Health, eLimu",
#         "deal_preferences": "Pre-seed to Seed, founder-led.",
#         "investment_thesis": "Supporting inclusive digital solutions from underserved regions.",
#         "engagement_style": "Mentorship-driven.",
#         "past_exits": "N/A",
#     },
#     {
#         "username": "equitycap",
#         "email": "team@equitycapital.co.ke",
#         "firm_name": "Equity Capital Partners",
#         "location": "Nakuru",
#         "check_size_min": 500000,
#         "check_size_max": 5000000,
#         "investment_focus": "Infrastructure, Logistics, Mobility",
#         "portfolio": "MoKo, Lori Systems",
#         "deal_preferences": "Series A and B, with exit potential.",
#         "investment_thesis": "Build scalable ventures with strong distribution.",
#         "engagement_style": "Board participation and funding rounds.",
#         "past_exits": "Sendy",
#     },
#     {
#         "username": "impactfusion",
#         "email": "contact@impactfusion.org",
#         "firm_name": "Impact Fusion",
#         "location": "Kisumu",
#         "check_size_min": 5000,
#         "check_size_max": 75000,
#         "investment_focus": "CivicTech, Women-led Startups",
#         "portfolio": "HerTech, VoteWise",
#         "deal_preferences": "Mission-driven with strong local traction.",
#         "investment_thesis": "Catalyzing social change through early support.",
#         "engagement_style": "Grant and hybrid capital.",
#         "past_exits": "N/A",
#     },
#     {
#         "username": "innovcapital",
#         "email": "hello@innovcapital.africa",
#         "firm_name": "InnovCapital Africa",
#         "location": "Nairobi",
#         "check_size_min": 25000,
#         "check_size_max": 100000,
#         "investment_focus": "AgriTech, GreenTech, EdTech",
#         "portfolio": "UjuziKilimo, GreenBox",
#         "deal_preferences": "Seed-stage with traction.",
#         "investment_thesis": "Investing in green and inclusive innovation.",
#         "engagement_style": "Remote advisory + capital.",
#         "past_exits": "FarmDrive",
#     },
# ]


# for i in investors:
#     if User.query.filter((User.username == i['username']) | (User.email == i['email'])).first():
#         print(f"⚠️ Skipping duplicate investor user: {i['username']}")
#         continue
#     print(f"✅ Adding Investor: {i['firm_name']}")
#     user = User(username=i['username'], email=i['email'], password=hashed_pw, role='investor')
#     db.session.add(user)
#     db.session.flush()
#     investor = Investor(
#         user_id=user.id,
#         firm_name=i['firm_name'],
#         location=i['location'],
#         check_size_min=i['check_size_min'],
#         check_size_max=i['check_size_max'],
#         investment_focus=i['investment_focus'],
#         portfolio=i['portfolio'],
#         deal_preferences=i['deal_preferences'],
#         investment_thesis=i['investment_thesis'],
#         engagement_style=i['engagement_style'],
#         past_exits=i['past_exits'],
#     )
#     db.session.add(investor)

# # Final commit
# try:
#     db.session.commit()
#     print("\n✅ Done! 5 startups and 5 investors added successfully.")
# except Exception as e:
#     print(f"\n❌ Error during commit: {e}")
#     db.session.rollback()










##### SEEDED startup1,investor1,mentor1,- 10####

# import os
# import random
# from faker import Faker
# from datetime import datetime, timedelta
# from app import create_app, db
# from app.models import User, Startup, Investor, Mentor
# import bcrypt

# # Setup
# app = create_app()
# fake = Faker()
# app.app_context().push()
# db.drop_all()
# db.create_all()

# # Global password
# password = 'test123'
# hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# # Upload folder
# UPLOAD_FOLDER = "static/uploads"

# # --- 1. Create Admin ---

# # --- Add dedicated admin user 'Jayson' ---
# jayson_admin = User(
#     username='Jayson',
#     email='jaysonocharo@students.uonbi.ac.ke',
#     password=bcrypt.hashpw('iwzhia_.21'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
#     role='admin',
#     approved=True,
#     bio=fake.text(),
#     linkedin_profile=fake.url(),
#     contact_info=fake.phone_number()
# )
# db.session.add(jayson_admin)


# admin = User(
#     username='admin',
#     email='admin@example.com',
#     password=hashed_pw,
#     role='admin',
#     approved=True
# )
# db.session.add(admin)

# # --- 2. Create Startups ---
# industries = ['FinTech', 'AgriTech', 'HealthTech', 'EdTech', 'E-Commerce']

# for i in range(1, 11):
#     user = User(
#         username=f"startup{i}",
#         email=f"startup{i}@test.com",
#         password=hashed_pw,
#         role='startup',
#         approved=True,
#         bio=fake.text(),
#         linkedin_profile=fake.url(),
#         contact_info=fake.phone_number()
#     )
#     db.session.add(user)
#     db.session.flush()  # Get user.id before creating startup

#     startup = Startup(
#         user_id=user.id,
#         company_name=fake.company(),
#         logo=f"{UPLOAD_FOLDER}/logo_{i}.png",
#         industry=random.choice(industries),
#         location=fake.city(),
#         founding_date=fake.date_between(start_date='-5y', end_date='-1y'),
#         team_size=random.randint(5, 50),
#         revenue_streams=fake.text(),
#         pricing_strategy=fake.text(),
#         customer_acquisition_cost=random.uniform(10, 200),
#         stage=random.choice(['Seed', 'Series A', 'Series B']),
#         funding_needed=random.uniform(50000, 500000),
#         valuation=random.uniform(100000, 5000000),
#         previous_funding=fake.sentence(),
#         revenue=random.uniform(10000, 500000),
#         mrr=random.uniform(1000, 100000),
#         user_growth=random.uniform(5, 50),
#         partnerships=fake.company(),
#         tech_stack=fake.words(nb=3, unique=True),
#         ip_rights="None yet",
#         competitive_advantage=fake.text(),
#         tam=random.uniform(1e6, 1e8),
#         sam=random.uniform(1e5, 1e7),
#         competition=fake.company(),
#         pitch_deck=f"{UPLOAD_FOLDER}/pitch_{i}.pdf",
#         demo_video=f"{UPLOAD_FOLDER}/demo_{i}.mp4",
#         website=fake.url(),
#         social_links=fake.url()
#     )
#     db.session.add(startup)

# # --- 3. Create Investors ---
# for i in range(1, 11):
#     user = User(
#         username=f"investor{i}",
#         email=f"investor{i}@test.com",
#         password=hashed_pw,
#         role='investor',
#         approved=True,
#         bio=fake.text(),
#         linkedin_profile=fake.url(),
#         contact_info=fake.phone_number()
#     )
#     db.session.add(user)
#     db.session.flush()

#     investor = Investor(
#         user_id=user.id,
#         firm_name=fake.company(),
#         location=fake.city(),
#         check_size_min=random.uniform(10000, 50000),
#         check_size_max=random.uniform(50000, 500000),
#         industry_focus=random.choice(industries),
#         stage_focus=random.choice(['Seed', 'Series A', 'Series B']),
#         portfolio=fake.text(),
#         deal_preferences=random.choice(['Equity', 'Debt', 'SAFE']),
#         investment_thesis=fake.text(),
#         engagement_style=random.choice(['Hands-on', 'Passive']),
#         past_exits=fake.company()
#     )
#     db.session.add(investor)

# # --- 4. Create Mentors ---
# for i in range(1, 11):
#     user = User(
#         username=f"mentor{i}",
#         email=f"mentor{i}@test.com",
#         password=hashed_pw,
#         role='mentor',
#         approved=True,
#         bio=fake.text(),
#         linkedin_profile=fake.url(),
#         contact_info=fake.phone_number()
#     )
#     db.session.add(user)
#     db.session.flush()

#     mentor = Mentor(
#         user_id=user.id,
#         expertise=fake.job(),
#         years_experience=random.randint(3, 20),
#         industry_focus=random.choice(industries),
#         mentorship_topics=", ".join(fake.words(nb=3)),
#         availability="Weekdays, 9am - 5pm"
#     )
#     db.session.add(mentor)

# # Commit everything
# db.session.commit()
# print("✅ Seeded 1 admin, 10 startups, 10 investors, and 10 mentors.")



# ## Seeding mentorship requests and mentorship sessions##

# from app import create_app, db
# from app.models import Startup, Mentor, MentorshipRequest, MentorshipSession
# from faker import Faker
# from datetime import datetime, timedelta
# import random

# # Setup
# app = create_app()
# app.app_context().push()
# fake = Faker()

# # --- 1. Seed Mentorship Requests ---

# print("🔁 Seeding mentorship requests...")

# all_startups = Startup.query.all()
# all_mentors = Mentor.query.all()

# for startup in all_startups:
#     selected_mentors = random.sample(all_mentors, k=2)  # each startup requests from 2 mentors
#     for mentor in selected_mentors:
#         req_date = fake.date_between(start_date='today', end_date='+30d')
#         req_time = (datetime.utcnow() + timedelta(hours=random.randint(9, 17))).time()
#         status = random.choice(['Pending', 'Accepted', 'Rejected'])

#         mentorship_request = MentorshipRequest(
#             startup_id=startup.id,
#             mentor_id=mentor.id,
#             request_date=req_date,
#             request_time=req_time,
#             status=status
#         )
#         db.session.add(mentorship_request)

# # --- 2. Seed Mentorship Sessions (only from accepted requests) ---

# print("📅 Seeding mentorship sessions from accepted requests...")

# accepted_requests = MentorshipRequest.query.filter_by(status='Accepted').all()

# for req in accepted_requests:
#     session = MentorshipSession(
#         mentor_id=req.mentor.user_id,
#         startup_id=req.startup.user_id,
#         date=datetime.combine(req.request_date, req.request_time),
#         status=random.choice(['Pending', 'Completed', 'Cancelled'])
#     )
#     db.session.add(session)

# db.session.commit()

# print("✅ Seeding complete: mentorship requests and sessions created.")

