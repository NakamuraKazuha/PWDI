import flet as ft
from sqlalchemy.orm import Session
from database import engine, Users

def consent_page(page, username, show_profile_setup):
    """Consent screen UI"""

    # Check if the user has already consented
    with Session(engine) as session:
        user = session.query(Users).filter_by(name=username).first()
        if user and user.consent:
            show_profile_setup(username)  # Skip consent page if already given
            return ft.Container()  # Return an empty container instead of None

    consent_checkbox = ft.Checkbox(label="I consent to the terms and conditions.")
    message = ft.Text("", color="red")

    def next_click(e):
        if consent_checkbox.value:
            # Store consent in the database
            with Session(engine) as session:
                user = session.query(Users).filter_by(name=username).first()
                if user:
                    user.consent = True
                    session.commit()

            show_profile_setup(username)  # Proceed to profile setup
        else:
            message.value = "You must consent to the terms and conditions."
            page.update()

    return ft.Container(
        width=page.width,
        height=page.height,
        bgcolor="#F0FAEF",
        border_radius=10,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Consent", text_align=ft.TextAlign.CENTER, color="#003B5B", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("Please read and accept our terms and conditions.", text_align=ft.TextAlign.CENTER, size=18),
                consent_checkbox,
                message,
                ft.ElevatedButton(
                    text="Next",
                    bgcolor="#003B5B",
                    color="white",
                    width=200,
                    height=50,
                    on_click=next_click,
                ),
            ],
        ),
    )
