from app import create_app, db
from app.models import MentorshipSession
from app.models import MentorshipRequest

app = create_app()

with app.app_context():
    # sessions = MentorshipSession.query.all()
    # print(sessions)
    
    requests = MentorshipRequest.query.all()
    print(requests)
    

