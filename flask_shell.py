from app import create_app, db
from app.models import Startup

# Initialize Flask app context
app = create_app()
app.app_context().push()

# Query the startup with ID=1
startup = Startup.query.get(1)

if startup:
    print(f"✅ Startup with ID=1 found: {startup.company_name}")
else:
    print("❌ No startup found with ID=1")
