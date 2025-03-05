import flet as ft
from welcome import welcome_page
from consent import consent_page
from profile import profile_setup_page
from medical import medical_mobility_page
from history import medical_history_page
from legal import legal_documentation_page
from splash import splash_screen
from first_interface import create_ui
from share import share  # Import the share function

def main(page: ft.Page):
    from login import login_page
    from signup import signup_page

    # Set Android phone screen size
    page.window.width = 412  # Standard width for Android phones
    page.window.height = 915  # Standard height for Android phones
    page.window.resizable = False
    page.bgcolor = "black"

    # Set fonts (from the second script)
    page.fonts = {
        "lalezar": "fonts/Lalezar-Regular.ttf",  # font
    }

    def show_login():
        page.clean()  # Clear the page before navigating
        page.add(login_page(page, show_signup, show_consent_page))

    def show_signup():
        page.clean()
        page.add(signup_page(page, show_login, show_consent_page))

    def show_consent_page(username):
        page.clean()
        page.add(consent_page(page, username, show_profile_setup))

    def show_profile_setup(username):
        page.clean()
        page.add(profile_setup_page(page, username, show_medical_mobility_page))

    def show_medical_mobility_page(username):
        page.clean()
        page.add(medical_mobility_page(page, username, show_medical_history_page))

    def show_medical_history_page(username):
        page.clean()
        page.add(medical_history_page(page, username, show_legal_documentation_page))

    def show_legal_documentation_page(username):
        page.clean()
        page.add(legal_documentation_page(page, username, show_main_ui))

    def show_welcome_page():
        page.clean()
        page.add(welcome_page(page, show_login, show_signup))

    def show_main_ui():
        page.clean()
        page.add(create_ui(page))

    # Define route change handler
    def route_change(route):
        page.views.clear()
        if page.route == "/":
            show_welcome_page()
        elif page.route == "/login":
            show_login()
        elif page.route == "/signup":
            show_signup()
        elif page.route == "/consent":
            show_consent_page("username")  # Replace with actual username if needed
        elif page.route == "/profile_setup":
            show_profile_setup("username")  # Replace with actual username if needed
        elif page.route == "/medical_mobility":
            show_medical_mobility_page("username")  # Replace with actual username if needed
        elif page.route == "/medical_history":
            show_medical_history_page("username")  # Replace with actual username if needed
        elif page.route == "/legal_documentation":
            show_legal_documentation_page("username")  # Replace with actual username if needed
        elif page.route == "/main_ui":
            show_main_ui()
        elif page.route == "/share":
            page.views.append(ft.View("/share", [share(page)]))  # Add the share page
        page.update()

    # Handle pop (back button)
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Set up route change and view pop handlers
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Start with the splash screen
    splash_screen(page, show_welcome_page)

ft.app(target=main, assets_dir="assets")
