import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    
    # PostgreSQL URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://Jayson:iwzhia_.21@localhost/digihub2postgre'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

