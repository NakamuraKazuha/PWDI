import flet as ft
import datetime
from database import SessionLocal, Profile, Users

def profile_setup_page(page, username, show_medical_mobility_page):
    """Profile setup screen UI"""
    page.title = "Profile Information"
    page.bgcolor = "#EDF8ED"

    # Background container (fills the entire page)
    background = ft.Container(
        content=ft.Image(
            src="assets/bgnew.jpg",
            fit=ft.ImageFit.COVER
        ),
        expand=True
    )
    
    # Logo container (centered at the top)
    logo = ft.Container(
        content=ft.Image(src="assets/logo1.png", width=150, height=150),
        alignment=ft.alignment.top_center,  # Center logo at the top
        margin=ft.margin.only(top=20)  # Add some top margin
    )

    first_name = ft.TextField(label="First Name", width=300, text_style=ft.TextStyle(color="#003B5B"))
    last_name = ft.TextField(label="Last Name", width=300, text_style=ft.TextStyle(color="#003B5B"))

    # Picks the date
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
        first_date=datetime.date(1900, 1, 1),
        last_date=datetime.date.today(),
    )
    
    dob_field = ft.TextField(label="Date of Birth", read_only=True, width=250, text_style=ft.TextStyle(color="#003B5B"))
    dob_picker_button = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=pick_date)
    dob_row = ft.Row(
        controls=[dob_field, dob_picker_button],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    address_field = ft.TextField(label="Address", width=300, text_style=ft.TextStyle(color="#003B5B"))
    contact_number_field = ft.TextField(label="Contact Number", width=300, text_style=ft.TextStyle(color="#003B5B"))

    message = ft.Text("", color="red")

    def save_profile(e):
        if not all([first_name.value, last_name.value, dob_field.value, address_field.value, contact_number_field.value]):
            message.value = "All fields must be filled."
            page.update()
            return

        try:
            with SessionLocal() as session:
                user = session.query(Users).filter(Users.name == username).first()
                if not user:
                    message.value = "User not found."
                    page.update()
                    return

                existing_profile = session.query(Profile).filter(Profile.id == user.user_id).first()
                if existing_profile:
                    message.value = "Profile already exists."
                    page.update()
                    return

                profile = Profile(
                    id=user.user_id,
                    username=user.name,
                    first_name=first_name.value.strip(),
                    last_name=last_name.value.strip(),
                    birth_date=datetime.datetime.strptime(dob_field.value, "%Y-%m-%d").date(),
                    address=address_field.value.strip(),
                    contact_number=contact_number_field.value.strip(),
                )

                session.add(profile)
                session.commit()

                show_medical_mobility_page(username)  # Proceed to the next page
        except Exception as ex:
            message.value = f"Error saving profile: {str(ex)}"
            page.update()

    page.overlay.append(birth_date_picker)
    page.update()

    return ft.Stack(
        controls=[
            background,  # Background image
            ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    logo,  # Centered logo at the top
                    ft.Text(
                        "Profile Setup",
                        text_align=ft.TextAlign.CENTER,
                        color="#003B5B",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    first_name,
                    last_name,
                    dob_row,
                    address_field,
                    contact_number_field,
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
            ),
        ]
    )
