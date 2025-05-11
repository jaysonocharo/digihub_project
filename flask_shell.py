from app import create_app, db
from app.models import User, Startup

# # Initialize Flask app context
app = create_app()
app.app_context().push()

#delete the 2 pairs of matching startups and investors
users = User.query.filter(User.email.like('match_%')).all()
for user in users:
    db.session.delete(user)
db.session.commit()



