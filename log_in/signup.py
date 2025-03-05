
import flet as ft
from navigation import register_user

def signup_page(page, show_login, show_consent_page):
    """Signup screen UI with separated containers"""

    # Background container
    background = ft.Container(
        content=ft.Image(
            src="assets/bgnew.jpg",
            fit=ft.ImageFit.FILL
        ),
        expand=True
    )

    # Logo container
    logo = ft.Container(
        content=ft.Image(src="assets/logo1.png", width=150, height=150),
        left=10,
        right=10,
        top=20
    )

    # Title container
    title = ft.Container(
        content=ft.Text(
            "Sign Up",
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

    # Username, email, and password fields
    username = ft.Container(
        content=ft.TextField(
            label="Enter Username",
            text_style=ft.TextStyle(color="#003B5B", font_family="Lalezar"),
            label_style=ft.TextStyle(color="#003B5B"),
            bgcolor="#F0FAEF",
            border=ft.InputBorder.NONE
        ),
        border_radius=8,
    )

    email = ft.Container(
        content=ft.TextField(
            label="Enter Email",
            text_style=ft.TextStyle(color="#003B5B", font_family="Lalezar"),
            label_style=ft.TextStyle(color="#003B5B"),
            bgcolor="#F0FAEF",
            border=ft.InputBorder.NONE
        ),
        border_radius=8,
    )

    password = ft.Container(
        content=ft.TextField(
            label="Password",
            password=True,
            text_style=ft.TextStyle(color="#003B5B", font_family="Lalezar"),
            label_style=ft.TextStyle(color="#003B5B"),
            bgcolor="#F0FAEF",
            border=ft.InputBorder.NONE
        ),
        border_radius=8,
    )

    message = ft.Text("", color="red")

    # Username label
    username_text = ft.Container(
        content=ft.Text(
            value="User Name",
            size=17,
            weight=ft.FontWeight.BOLD,
            color="#003B5B",
            font_family="Lalezar",
        ),
        left=20,
        top=300
    )

    # Email label
    email_text = ft.Container(
        content=ft.Text(
            value="Email",
            size=17,
            weight=ft.FontWeight.BOLD,
            color="#003B5B",
            font_family="Lalezar",
        ),
        left=20,
        top=390
    )

    # Password label
    password_text = ft.Container(
        content=ft.Text(
            value="Password",
            size=17,
            weight=ft.FontWeight.BOLD,
            color="#003B5B",
            font_family="Lalezar",
        ),
        left=20,
        top=480
    )

    # Remember me checkbox
    remember_me = ft.Container(
    content=ft.Row(
        [
            ft.Checkbox(
                label="Remember me",
                label_style=ft.TextStyle(color="#003B5B")  # Change text color
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER
    ),
    top=570,
    left=50,
    right=50
)



    # Signup button
    def signup_click(e):
        success, msg = register_user(username.content.value, email.content.value, password.content.value)
        message.value = msg
        message.color = "green" if success else "red"
        page.update()
        if success:
            show_consent_page(username.content.value)  # Pass the username to the consent page

    signup_button = ft.Container(
        content=ft.ElevatedButton(
            text="Continue",
            bgcolor="#003B5B",
            color="white",
            width=200,
            height=50,
            on_click=signup_click,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)  # Change the radius as needed
            ),
        ),
        top=620,  
        left=0,
        right=0,
        alignment=ft.alignment.center
    )

    # Login link
    login_link = ft.Container(
        content=ft.TextButton(
            "Already have an account? Log In",
            on_click=lambda e: show_login(),
            style=ft.ButtonStyle(color="#003B5B")  
        ),
        top=690,
        left=0,
        right=0,
        alignment=ft.alignment.center
    )

    # Input fields container
    input_fields = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=40,
            controls=[username, email, password, message]
        ),
        top=335,
        left=50,
        right=50,
    )

    # Combine everything into a Stack
    return ft.Stack(
        controls=[background, logo, username_text, email_text, password_text, title, input_fields, remember_me, signup_button, login_link],
        width=page.window.width,
        height=page.window.height
    )
