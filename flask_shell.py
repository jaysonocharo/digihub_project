# ##   delete and add user
# from app import create_app, db
# from app.models import User
# from flask_bcrypt import Bcrypt

# app = create_app()
# bcrypt = Bcrypt(app)

# with app.app_context():
#     user = User.query.filter_by(email="jaysonocharo@students.uonbi.ac.ke").first()
#     if user:
#         db.session.delete(user)
#         db.session.commit()
#         print("🗑️ Old admin deleted.")

#     admin = User(
#         username="jayson",
#         email="jaysonocharo@students.uonbi.ac.ke",
#         password=bcrypt.generate_password_hash("iwzhia_.21").decode('utf-8'),
#         role="admin",
#         approved=True
#     )
#     db.session.add(admin)
#     db.session.commit()
#     print("✅ New admin created with bcrypt.")

##Change password
# flask_shell.py
from app import create_app, db
from app.models import User
from flask_bcrypt import Bcrypt

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    # Replace with your target email
    user = User.query.filter_by(email="kaitlin39@example.org").first()

    if user:
        print(f"👤 Found user: {user.username} | role: {user.role}")
        
        # Optional: reset the password to something you know
        user.password = bcrypt.generate_password_hash("newpassword123").decode('utf-8')
        db.session.commit()
        print("✅ Password has been reset to 'newpassword123'.")
    else:
        print("❌ User not found.")

