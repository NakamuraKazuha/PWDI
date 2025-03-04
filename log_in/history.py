import flet as ft
from sqlalchemy.orm import sessionmaker
from database import engine, MedicalHistory, Users

Session = sessionmaker(bind=engine)
session = Session()

def medical_history_page(page, username, show_legal_documentation_page):
    """Medical History Information page UI"""
    primary_diagnosis = ft.TextField(label="Enter Diagnosis", expand=True)
    other_conditions = ft.TextField(label="Optional", expand=True)

    # Medication inputs
    medication_name = ft.TextField(label="Add Medication", expand=1)
    medication_dosage = ft.TextField(label="Dosage", expand=1)
    medication_frequency = ft.TextField(label="Frequency", expand=1)

    # Allergies
    allergies = ft.TextField(label="Enter Allergies", expand=True)

    # Past surgeries
    surgery_year = ft.TextField(label="Year", expand=1)
    surgery_name = ft.TextField(label="Procedure Name", expand=2)
    hospital_name = ft.TextField(label="Hospital Name", expand=2)

    message = ft.Text("", color="red")

    def next_click(e):
        if primary_diagnosis.value:
            # Retrieve the user_id from the username
            user = session.query(Users).filter_by(name=username).first()
            
            if user is None:
                message.value = "User not found in the database."
                page.update()
                return

            # Store data into the database
            new_entry = MedicalHistory(
                user_id=user.user_id,  # Store the actual user_id
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

            # Redirect to next page
            show_legal_documentation_page(username)
        else:
            message.value = "Please provide your primary diagnosis."
            page.update()

    return ft.Container(
        width=page.width,
        height=page.height,
        bgcolor="#F0FAEF",
        border_radius=10,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("Medical History", text_align=ft.TextAlign.CENTER, color="#003B5B", size=24, weight=ft.FontWeight.BOLD),
                
                ft.Text("Primary Diagnosis", weight=ft.FontWeight.BOLD),
                primary_diagnosis,

                ft.Text("Other Medical Conditions", weight=ft.FontWeight.BOLD),
                other_conditions,

                ft.Text("Current Medications", weight=ft.FontWeight.BOLD),
                ft.Row([medication_name, medication_dosage, medication_frequency], spacing=10),

                ft.Text("Allergies", weight=ft.FontWeight.BOLD),
                allergies,

                ft.Text("Past Surgeries", weight=ft.FontWeight.BOLD),
                ft.Row([surgery_year, surgery_name, hospital_name], spacing=10),

                message,
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=10),
                    content=ft.ElevatedButton(text="Next", bgcolor="#003B5B", color="white", width=200, height=50, on_click=next_click),
                ),
            ],
        ),
    )
