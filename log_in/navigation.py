import flet as ft
BASE_URL = "http://127.0.0.1:5000"

def register_user(username, email, password):
    """Mock function to register a user (no API call)."""
    if username and email and password:
        return True, "Registration successful!"
    return False, "Registration failed. Please fill all fields."

def authenticate_user(username, password):
    """Mock function to authenticate a user (no API call)."""
    if username == "admin" and password == "password":
        return True, "Login successful!"
    return False, "Invalid username or password."
