import flet as ft
from sqlalchemy.orm import sessionmaker
from database import engine, Users

Session = sessionmaker(bind=engine)
session = Session()

def legal_documentation_page(page, username, on_submit):
    """Legal and Documentation page UI"""
    
    page.title = "Legal & Documentation"
    page.bgcolor = "#F0FAEF"  # Consistent background color

    # Background Image
    background = ft.Container(
        content=ft.Image(src="assets/bgnew.jpg", fit=ft.ImageFit.COVER),
        expand=True
    )

    # Logo
    logo = ft.Image(src="assets/logo1.png", width=120, height=120)

    legal_terms_checkbox = ft.Checkbox(
    label="I agree to the legal terms and conditions.",
    label_style=ft.TextStyle(color="#003B5B")  # Change color to dark blue
)
    message = ft.Text("", color="red")

    def submit_click(e):
        if legal_terms_checkbox.value:
            # Retrieve the user by name
            user = session.query(Users).filter_by(name=username).first()

            if user:
                user.legal = True  # Store that the user has agreed
                session.commit()

                message.value = "All steps completed. Thank you for your submission!"
                message.color = "green"
                page.update()

                # Navigate to the first interface after a short delay
                page.clean()
                on_submit(username)  # Call the callback to navigate to the first interface
            else:
                message.value = "User not found in the database."
                message.color = "red"
        else:
            message.value = "You must agree to the legal terms."
            message.color = "red"
        
        page.update()

    return ft.Stack(
        controls=[
            background,
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo,
                    ft.Text(
                        "Legal & Documentation",
                        text_align=ft.TextAlign.CENTER,
                        color="#003B5B",  # Dark blue color for consistency
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "Please read and accept the legal terms before submitting.",
                        text_align=ft.TextAlign.CENTER,
                        size=18,
                        color="#003B5B",  # Dark blue color for better readability
                    ),
                    legal_terms_checkbox,
                    message,
                    ft.ElevatedButton(
                        text="Submit",
                        bgcolor="#003B5B",
                        color="white",
                        width=200,
                        height=50,
                        on_click=submit_click,
                    ),
                ],
            ),
        ]
    )
