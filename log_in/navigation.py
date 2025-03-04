import random
from werkzeug.security import generate_password_hash, check_password_hash
from database import session, Users

def generate_unique_user_id():
    """Generate a unique 6-digit user_id."""
    while True:
        user_id = random.randint(00000, 999999)  # Generate user_id
        if not session.query(Users).filter_by(user_id=user_id).first():  # Ensure it's unique
            return user_id

def register_user(username, email, password):
    """Registers a new user with hashed password and unique 6-digit user_id"""
    if session.query(Users).filter_by(name=username).first():
        return False, "Username already exists"
    
    hashed_password = generate_password_hash(password)
    
    new_user = Users(
        user_id=generate_unique_user_id(),  #assign
        name=username, 
        email=email, 
        password_hash=hashed_password
    ) 
    session.add(new_user)
    session.commit()
    
    return True, "Registration successful"

def authenticate_user(username, password):
    user = session.query(Users).filter_by(name=username).first()  
    if user and check_password_hash(user.password_hash, password):
        return True, "Login successful!"
    return False, "Invalid username or password."
