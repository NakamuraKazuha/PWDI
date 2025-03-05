from profile_page import create_profile_ui
from share import share_page

def emergency_button(e):
    print("Emergency Button!")

def share_button(e, username):
    e.page.clean()  
    e.page.add(share_page(e.page, username))
    e.page.update()

def home_button(e):
    print("Home Button")

def profile(e):
    e.page.clean() 
    e.page.add(create_profile_ui(e.page))  
    e.page.update()

def notif(e):
    print("Notification")

def medical(e):
    print("Medical and Mobility Information")

def medical_history(e):
    print("Medical History")

def legal_docu(e):
    print("Legal & Documentation")

def edit_profile(e):
    print("Edit Profile")
