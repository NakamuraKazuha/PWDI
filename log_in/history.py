import flet as ft
from sqlalchemy.orm import sessionmaker
from database import engine, MedicalHistory, Users

Session = sessionmaker(bind=engine)
session = Session()

def medical_history_page(page, username, show_legal_documentation_page):
    """Medical History Information page UI"""

    page.title = "Medical History"
    page.bgcolor = "#F0FAEF"

    # Background Image
    background = ft.Container(
        content=ft.Image(src="assets/bgnew.jpg", fit=ft.ImageFit.COVER),
        expand=True
    )

    # Logo
    logo = ft.Image(src="assets/logo1.png", width=120, height=120)

    # Input Fields
    primary_diagnosis = ft.TextField(label="Enter Diagnosis", width=350)
    other_conditions = ft.TextField(label="Optional", width=350)

    medication_name = ft.TextField(label="Medication", width=120)
    medication_dosage = ft.TextField(label="Dosage", width=110)
    medication_frequency = ft.TextField(label="Frequency", width=120)

    allergies = ft.TextField(label="Enter Allergies", width=350)

    surgery_year = ft.TextField(label="Year", width=100)
    surgery_name = ft.TextField(label="Procedure", width=150)
    hospital_name = ft.TextField(label="Hospital Name", width=110)

    message = ft.Text("", color="red")

    def next_click(e):
        if primary_diagnosis.value:
            user = session.query(Users).filter_by(name=username).first()
            
            if user is None:
                message.value = "User not found in the database."
                page.update()
                return

            new_entry = MedicalHistory(
                user_id=user.user_id,  
                primary_diagnosis=primary_diagnosis.value,
                other_conditions=other_conditions.value,
                medication_name=medication_name.value,
                medication_dosage=medication_dosage.value,
                medication_frequency=medication_frequency.value,
                allergies=allergies.value,
                surgery_year=surgery_year.value,
                surgery_name=surgery_name.value,
                hospital_name=hospital_name.value
            )

            session.add(new_entry)
            session.commit()

            show_legal_documentation_page(username)
        else:
            message.value = "Please provide your primary diagnosis."
            page.update()

    return ft.Stack(
        controls=[
            background,
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo,
                    ft.Text("Medical History", text_align=ft.TextAlign.CENTER, color="#003B5B", size=24, weight=ft.FontWeight.BOLD),
                    
                    ft.Text("Primary Diagnosis:", color="#003B5B", weight=ft.FontWeight.BOLD),
                    primary_diagnosis,

                    ft.Text("Other Medical Conditions:", color="#003B5B", weight=ft.FontWeight.BOLD),
                    other_conditions,

                    ft.Text("Current Medications:", color="#003B5B", weight=ft.FontWeight.BOLD),
                    ft.Row([medication_name, medication_dosage, medication_frequency], spacing=15),  # Adjusted spacing

                    ft.Text("Allergies:", color="#003B5B", weight=ft.FontWeight.BOLD),
                    allergies,

                    ft.Text("Past Surgeries:", color="#003B5B", weight=ft.FontWeight.BOLD),
                    ft.Row([surgery_year, surgery_name, hospital_name], spacing=15),  # Adjusted spacing

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
        ]
    )
