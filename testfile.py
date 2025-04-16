from app import create_app, db
from app.models import MentorshipSession


app = create_app()

with app.app_context():
    sessions = MentorshipSession.query.all()
    print(sessions)

