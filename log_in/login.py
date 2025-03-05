import flet as ft
from navigation import authenticate_user

def login_page(page, show_signup, show_consent_page):
    """Login screen UI with separated containers"""

    background = ft.Container(
        content=ft.Image(
            src="assets/bgnew.jpg",
            fit=ft.ImageFit.FILL
        ),
        expand=True
    )

    logo = ft.Container(
        content=ft.Image(src="assets/logo1.png", width=150, height=150),
        left=10,
        right=10,
        top=20
    )

    title = ft.Container(
        content=ft.Text(
            "Log In",
            text_align=ft.TextAlign.CENTER,
            color="#003B5B",
            size=24,
            weight=ft.FontWeight.BOLD,
        ),
        top=200,
        left=0,
        right=0,
        alignment=ft.alignment.center
    )
    
    username = ft.TextField(
        label="Enter Username",
        text_style=ft.TextStyle(color="#003B5B", font_family="Lalezar"),
        label_style=ft.TextStyle(color="#003B5B"),
        bgcolor="#F0FAEF",
        border=ft.InputBorder.NONE
    )
    
    password = ft.TextField(
        label="Password",
        password=True,
        text_style=ft.TextStyle(color="#003B5B", font_family="Lalezar"),
        label_style=ft.TextStyle(color="#003B5B"),
        bgcolor="#F0FAEF",
        border=ft.InputBorder.NONE
    )
    
    message = ft.Text("", color="red")
    
    def login_click(e):
        success, msg = authenticate_user(username.value, password.value)
        message.value = msg
        message.color = "green" if success else "red"
        page.update()
        if success:
            show_consent_page(username.value)
    
    login_button = ft.ElevatedButton(
        text="Log In",
        bgcolor="#003B5B",
        color="white",
        width=200,
        height=50,
        on_click=login_click,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )
    
    signup_link = ft.TextButton(
        "New to PWDI? Sign Up",
        on_click=lambda e: show_signup(),
        style=ft.ButtonStyle(color="#003B5B")
    )
    
    username_text = ft.Text(
        value="User Name",
        size=17,
        weight=ft.FontWeight.BOLD,
        color="#003B5B",
        font_family="Lalezar",
    )
    
    password_text = ft.Text(
        value="Password",
        size=17,
        weight=ft.FontWeight.BOLD,
        color="#003B5B",
        font_family="Lalezar",
    )
    
    input_fields = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40,
            controls=[username, password, message],
        ),
        top=335,
        left=50,
        right=50,
    )
    
    return ft.Stack(
        controls=[
            background, logo, username_text, password_text, title, 
            input_fields, login_button, signup_link
        ],
        width=page.window.width,
        height=page.window.height
    )
