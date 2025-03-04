import flet as ft
import datetime
from database import SessionLocal, Profile, Users
import datetime

def profile_setup_page(page, username, show_medical_mobility_page):
    """Profile setup screen UI"""
    page.title = "Profile Information"
    page.bgcolor = "#EDF8ED"
    page.padding = 20

    first_name = ft.TextField(label="First Name", width=300)
    last_name = ft.TextField(label="Last Name", width=300)

     #picks the date
    def update_dob_field(e):
        if birth_date_picker.value:
            selected_date = birth_date_picker.value.date()  # Convert to date
            today = datetime.date.today()

            if selected_date > today:
                dob_field.value = "Invalid date."
                dob_field.color = "red"
            else:
                dob_field.value = selected_date.strftime("%Y-%m-%d")
            page.update()

    
    def pick_date(e):
        page.open(birth_date_picker)  

    birth_date_picker = ft.DatePicker(
        on_change=update_dob_field,
        first_date=datetime.date(1900, 1, 1),  #earliest possible date
        last_date=datetime.date.today(),  #cant do past this
    )
    
    dob_field = ft.TextField(label="Date of Birth", read_only=True, width=250)
    dob_picker_button = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=pick_date)
    dob_row = ft.Row(
        controls=[dob_field, dob_picker_button],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )
    message = ft.Text("", color="red")

    def save_profile(e):
        if first_name.value and last_name.value and dob_field.value:
            with SessionLocal() as session:

                # Fetch user_id
                user = session.query(Users).filter(Users.name == username).first()
                if not user:
                    message.value = "User not found."
                    page.update()
                    return

                profile = Profile(
                    id=user.user_id,  # Use existing user_id from Users
                    username=user.name,  # Use existing username from Users
                    first_name=first_name.value.strip(),
                    last_name=last_name.value.strip(),
                    birth_date=datetime.datetime.strptime(dob_field.value, "%Y-%m-%d").date(),
                )

                session.add(profile)
                session.commit()

            show_medical_mobility_page(username)  # Proceed to the next page
        else:
            message.value = "All fields must be filled."
            page.update()

    page.overlay.append(birth_date_picker)  #DatePicker is in overlay
    page.update()
    
    return ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Profile Setup",
                text_align=ft.TextAlign.CENTER,
                color="#003B5B",
                size=24,
                weight=ft.FontWeight.BOLD,
            ),
            first_name,
            last_name,
            dob_row,  # Date of Birth Field with Button
            message,
            ft.ElevatedButton(
                text="Save Profile",
                bgcolor="#006A8E",
                color="white",
                width=200,
                height=50,
                on_click=save_profile,
            ),
        ],
    )
