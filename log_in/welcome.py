import flet as ft

def welcome_page(page, show_login, show_signup):
    """Landing page with Log in and Sign up buttons"""

    # Background container with image
    background = ft.Container(
        expand=True,
        content=ft.Image(
            src="assets/bgnew.jpg",
            fit=ft.ImageFit.COVER
        )
    )

    # Title positioned manually
    title = ft.Container(
        content=ft.Text(
            "PWD Independence",
            text_align=ft.TextAlign.CENTER,
            color="#003B5B",
            size=28,
            weight=ft.FontWeight.BOLD,
        ),
        left=50,  # Adjust X-axis position
        top=100   # Adjust Y-axis position
    )

    # Log in button positioned manually
    login_button = ft.Container(
        content=ft.ElevatedButton(
            text="Log in",
            bgcolor="#003B5B",
            color="white",
            width=200,
            height=50,
            on_click=lambda e: show_login(),
        ),
        left=100,
        top=200
    )

    # Sign up button positioned manually
    signup_button = ft.Container(
        content=ft.ElevatedButton(
            text="Sign up",
            bgcolor="#006A8E",
            color="white",
            width=200,
            height=50,
            on_click=lambda e: show_signup(),
        ),
        left=100,
        top=270  # Placed slightly below Log in button
    )

    return ft.Stack(
        controls=[background, title, login_button, signup_button]
    )
