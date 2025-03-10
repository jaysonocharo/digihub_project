# **DIGIHUB: Digital Innovation Hub Portal**

## **Project Overview**
DIGIHUB is a web-based platform designed to connect Kenyan startups, investors, mentors, and government innovation programs. The platform facilitates mentorship, investor-startup matching, and administrative oversight.

## **Features**
✅ User Authentication & Role-Based Access (Startup, Investor, Mentor, Admin)  
✅ Startup Registration & Profile Management  
✅ Investor-Startup Matching System  
✅ Mentorship Scheduling & Approvals  
✅ Admin Dashboard for User Management  
✅ In-App Notifications  
✅ Search & Filtering System  
✅ Activity Logs for Admins  

---

## **Tech Stack**
- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, Jinja, JavaScript
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Form Handling:** Flask-WTF

---

## **Installation & Setup**
### **1. Clone the Repository**
```bash
git clone https://github.com/yourrepo/digihub.git
cd digihub
```

### **2. Create a Virtual Environment**
```bash
python -m venv venv
```

### **3. Activate the Virtual Environment**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### **4. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **5. Set Up Database**
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### **6. Run the App**
```bash
flask run
```

### **7. Open in Browser**
Visit **http://127.0.0.1:5000/** to access the platform.

---

## **Usage Guide**
### **1. User Roles & Features**
- **Startups:** Register, manage profiles, apply for mentorship, get matched with investors.
- **Investors:** Browse startups, invest in relevant businesses.
- **Mentors:** Approve/reject mentorship requests, provide guidance.
- **Admins:** Manage users, approve startups, monitor logs.

### **2. Important Routes**
| Route                 | Description                          |
|----------------------|----------------------------------|
| `/register`         | Register a new user              |
| `/login`            | Login to the platform            |
| `/dashboard`        | User dashboard (based on role)  |
| `/mentorship`       | Request mentorship session      |
| `/matches`          | View startup-investor matches   |
| `/admin_dashboard`  | Admin control panel             |
| `/activity_logs`    | View admin activity logs        |

---

## **Testing**
To run automated tests, execute:
```bash
pytest test_app.py
```
Expected output: All tests should pass successfully.

---

## **Deployment Guide**
For production deployment, use **Gunicorn**:
```bash
pip install gunicorn

gunicorn -w 4 run:app
```

Alternatively, deploy on **PythonAnywhere** or **Heroku** following their Flask deployment guides.

---

## **Troubleshooting**
### **Common Issues & Fixes**
❌ *Flask-Migrate error (`no such command 'db'`)*  
✅ Ensure `flask_migrate` is installed and `Migrate(app, db)` is initialized in `__init__.py`.

❌ *Virtual Environment Activation Fails*  
✅ Use `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).

❌ *Static files (CSS, JS, Images) not loading*  
✅ Make sure the `url_for('static', filename='path/to/file')` is correctly referenced in templates.

---

## **Contributors**
- **Mogaka Jayson Ocharo** *(Lead Developer)*
- **Supervisor:** Prof. Robert Oboko

---

## **License**
This project is licensed under the MIT License. Feel free to contribute and improve!

---

🚀 **DIGIHUB - Empowering Startups in Kenya!**

