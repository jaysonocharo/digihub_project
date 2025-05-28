#for running flask files such as for the database migrations
# flask_shell.py

from app import create_app, db, bcrypt
from app.models import User, Startup
from app import db
from app.models import Investor, User
from app.matching import match_startups_to_investors

app = create_app()
app.app_context().push()



scalemeup = Startup.query.filter_by(company_name='ScaleMeUp').first()
if scalemeup:
    print("📧 Email of ScaleMeUp:", scalemeup.user.email)
else:
    print("❌ ScaleMeUp not found in database.")