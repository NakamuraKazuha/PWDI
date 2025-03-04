import flet as ft
from navigation import register_user

def signup_page(page, show_login, show_consent_page):
    """Signup screen UI"""
    username = ft.TextField(label="Username", icon=ft.icons.PERSON)
    email = ft.TextField(label="Email", icon=ft.icons.EMAIL)
    password = ft.TextField(label="Password", password=True, icon=ft.icons.LOCK)
    message = ft.Text("", color="red")

    def signup_click(e):
        success, msg = register_user(username.value, email.value, password.value)
        message.value = msg
        message.color = "green" if success else "red"
        page.update()
        if success:
            show_consent_page(username.value)  # Pass the username to the consent page

    return ft.Container(
        width=page.width,
        height=page.height,
        bgcolor="#F0FAEF",
        border_radius=10,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Sign Up",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                username,
                email,
                password,
                ft.Row(
                    [ft.Checkbox(label="Remember me")],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.ElevatedButton(
                    text="Continue",
                    bgcolor="#006A8E",
                    color="white",
                    width=200,
                    height=50,
                    on_click=signup_click,
                ),
                message,
                ft.TextButton(
                    "Already have an account? Log in",
                    on_click=lambda e: show_login(),
                ),
            ],
        ),
    )
