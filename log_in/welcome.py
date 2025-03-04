
from flet import *

def welcome_page(page, show_login, show_signup):
    """Landing page with Log in and Sign up buttons"""

    # Background container with image
    background = Container(
        content=Image(
            src="assets/bgnew.jpg",
            fit=ImageFit.FILL
        ),
        expand=True
    )

    logo = Container(
        content=Image(src="assets/logo1.png", width=300, height=250),
        left=10,
        right=10,
        top=50
    )

   

    # Log in button positioned manually
    login_button = Container(
    content=ElevatedButton(
        text="Log in",
        bgcolor="#F0FAEF",
        color="#003B5B",
        width=200,
        height=50,
        on_click=lambda e: show_login(),
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8) ,
            text_style=TextStyle(
                    size=20,
                    weight=FontWeight.BOLD,
                    font_family="Lalezar"
                ) 
        )
    ),
    left=50,
    right=50,
    top=370
)

    # Sign up button positioned manually
    signup_button =Container(
        content=ElevatedButton(
            text="Sign up",
            bgcolor="#F0FAEF",
            color="#003B5B",
            width=200,
            height=50,
            on_click=lambda e: show_signup(),
            style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8),
            text_style=TextStyle(
                    size=20,
                    weight=FontWeight.BOLD,
                    font_family="Lalezar"
                )   # Move shape inside ButtonStyle
        )
        ),
        left=50,
        right=50,
        top=450
    )

    return Stack(
        controls=[background, logo, login_button, signup_button],
        width=page.window.width,
        height=page.window.height
    )
