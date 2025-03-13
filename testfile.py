from app import create_app, db
from app.models import MentorshipSession

# Create Flask app instance
app = create_app()

# Run inside the application context
with app.app_context():
    sessions = MentorshipSession.query.all()
    print(sessions)

