import string
import re
from datetime import datetime
from flask_bcrypt import Bcrypt

EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
USER_PATTERN = r"^[a-zA-Z0-9_]{3,20}$"
bcrypt = Bcrypt()


def valid_email(email:str):
    return email and bool(re.fullmatch(EMAIL_PATTERN, email))

def valid_username(user:str):
    return user and bool(re.fullmatch(USER_PATTERN, user))

def valid_password(password: str):
    if len(password) <= 5:
        return False, "The password must be at least 6 characters long."
    
    if not any(char.isdigit() for char in password):
        return False, "The password must contain at least one digit."
    
    if not any(char.isalpha() for char in password):
        return False, "The password must contain at least one letter."
    
    if not any(char in string.punctuation for char in password):
        return False, "The password must contain at least one special character."
    
    return True, "Password is valid."
    
def valid_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return None

def encrypt_password(password_original:str):
    return bcrypt.generate_password_hash(password_original).decode('utf-8')

def check_password(password:str, hashed_password:str):
    return bcrypt.check_password_hash(hashed_password, password)
