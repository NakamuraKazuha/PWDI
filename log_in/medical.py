import flet as ft
from sqlalchemy.orm import sessionmaker
from database import engine, Profile 

Session = sessionmaker(bind=engine)
session = Session()

def medical_mobility_page(page, username, show_medical_history_page):
    """Medical and Mobility Information page UI"""

    page.title = "Medical & Mobility Information"
    page.bgcolor = "#F0FAEF"

    # Background Image
    background = ft.Container(
        content=ft.Image(src="assets/bgnew.jpg", fit=ft.ImageFit.COVER),
        expand=True
    )

    # Logo
    logo = ft.Container(
        content=ft.Image(src="assets/logo1.png", width=120, height=120),
        alignment=ft.alignment.center
    )

    # Medical Conditions List
    medical_conditions = [
        "Psychological Disability",
        "Mental Disability",
        "Hearing Disability",
        "Visual Disability",
        "Learning Disability",
        "Speech Impairment",
        "Orthopedic Disability"
    ]

    medical_condition = ft.RadioGroup(
    content=ft.Column(
        [
            ft.Radio(
                value=condition, 
                label=condition, 
                label_style=ft.TextStyle(color="#003B5B", font_family="Lalezar")  # Change color here
            ) 
            for condition in medical_conditions
        ],
        alignment=ft.MainAxisAlignment.START
    )
)

    # Mobility Issues TextField
    mobility_issue = ft.TextField(
        label="Mobility Issues (if any)",
        width=300,
        text_style=ft.TextStyle(color="black")
    )

    # Message Display
    message = ft.Text("", color="red")

    # Next Button Click Event
    def next_click(e):
        if medical_condition.value or mobility_issue.value:
            profile = session.query(Profile).filter_by(username=username).first()
            if profile:
                profile.medical_condition = medical_condition.value if medical_condition.value else None
                profile.mobility_issues = mobility_issue.value if mobility_issue.value else None
                session.commit()
                print(f"Updated Profile: {username}, Medical: {profile.medical_condition}, Mobility: {profile.mobility_issues}")
            else:
                print("Profile not found!")

            show_medical_history_page(username)
        else:
            message.value = "Please provide information about your medical and mobility issues."
            page.update()

    # Main Content
    form_container = ft.Container(
        padding=ft.padding.all(20),
        width=350,
        bgcolor="#F0FAEF",
        border_radius=10,
        shadow=ft.BoxShadow(blur_radius=5, color=ft.colors.GREY_400),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Medical & Mobility Information",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text("Type of Disability:", color="black"),
                medical_condition,
                mobility_issue,
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
        )
    )

    return ft.Stack(
        controls=[
            background,
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[logo, form_container]
            )
        ]
    )
