#for running flask files such as for the database migrations
from app import create_app, db
from app.models import User, Startup

app = create_app()
app.app_context().push()

from app.models import Startup
db.session.get(Startup, 54)






