import flet as ft
from navigation import authenticate_user

def login_page(page, show_signup, show_consent_page):
    """Login screen UI"""
    username = ft.TextField(label="Username", icon=ft.icons.PERSON)
    password = ft.TextField(label="Password", password=True, icon=ft.icons.LOCK)
    message = ft.Text("", color="red")

    def login_click(e):
        success, msg = authenticate_user(username.value, password.value)
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
                    "Log in",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                username,
                password,
                ft.ElevatedButton(
                    text="Log in",
                    bgcolor="#003B5B",
                    color="white",
                    width=200,
                    height=50,
                    on_click=login_click,
                ),
                message,
                ft.TextButton(
                    "New to PWD? Sign up",
                    on_click=lambda e: show_signup(),
                ),
            ],
        ),
    )
