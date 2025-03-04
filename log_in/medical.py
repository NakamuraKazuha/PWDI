import flet as ft
from sqlalchemy.orm import sessionmaker
from database import engine, Profile 

Session = sessionmaker(bind=engine)
session = Session()

def medical_mobility_page(page, username, show_medical_history_page):
    """Medical and Mobility Information page UI"""
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
        content=ft.Column([
            ft.Radio(value=condition, label=condition) for condition in medical_conditions
        ])
    )
    
    mobility_issue = ft.TextField(label="Mobility Issues (if any)")
    message = ft.Text("", color="red")

    def next_click(e):
        if medical_condition.value or mobility_issue.value:
            # Fetch the user profile
            profile = session.query(Profile).filter_by(username=username).first()
            if profile:
                profile.medical_condition = medical_condition.value if medical_condition.value else None
                profile.mobility_issues = mobility_issue.value if mobility_issue.value else None
                session.commit()  # Save changes
                print(f"Updated Profile: {username}, Medical: {profile.medical_condition}, Mobility: {profile.mobility_issues}")
            else:
                print("Profile not found!")

            show_medical_history_page(username)
        else:
            message.value = "Please provide information about your medical and mobility issues."
            message.color = "red"
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
                ft.Text(
                    "Medical & Mobility Information",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text("Type of Disability:"),
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
        ),
    )
