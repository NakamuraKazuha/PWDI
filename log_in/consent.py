import flet as ft
from sqlalchemy.orm import Session
from database import engine, Users

def consent_page(page, username, show_profile_setup):
    """Consent screen UI with database integration"""

    with Session(engine) as session:
        user = session.query(Users).filter_by(name=username).first()
        if user and user.consent:
            show_profile_setup(username)
            return ft.Container()
    
    background = ft.Container(
        content=ft.Image(
            src="assets/bgnew.jpg",
            fit=ft.ImageFit.FILL
        ),
        expand=True
    )
    
    title = ft.Container(
        content=ft.Text(
            "Consent",
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
    
    info_text = ft.Container(
        content=ft.Text(
            "Please read and accept our terms and conditions.",
            text_align=ft.TextAlign.CENTER,
            size=18,
            color="#003B5B",
        ),
        top=250,
        left=20,
        right=20,
        alignment=ft.alignment.center
    )
    
    consent_checkbox = ft.Checkbox(
    label="I consent to the terms and conditions.",
    label_style=ft.TextStyle(color="#003B5B")  # Change this to your desired color
)
    message = ft.Text("", color="red")

    def next_click(e):
        if consent_checkbox.value:
            with Session(engine) as session:
                user = session.query(Users).filter_by(name=username).first()
                if user:
                    user.consent = True
                    session.commit()
            show_profile_setup(username)
        else:
            message.value = "You must consent to the terms and conditions."
            page.update()
    
    consent_container = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                consent_checkbox,
                message,
                ft.ElevatedButton(
                    text="Next",
                    bgcolor="#003B5B",
                    color="white",
                    width=200,
                    height=50,
                    on_click=next_click,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8)
                    ),
                ),
            ],
        ),
        top=300,
        left=50,
        right=50,
    )
    
    return ft.Stack(
        controls=[background, title, info_text, consent_container],
        width=page.window.width,
        height=page.window.height
    )
