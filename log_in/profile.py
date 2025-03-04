import flet as ft

def profile_setup_page(page, username, show_medical_mobility_page):
    """Profile setup screen UI"""
    page.title = "Profile Information"
    page.bgcolor = "#EDF8ED"
    page.padding = 20

    first_name = ft.TextField(label="First Name", width=300)
    last_name = ft.TextField(label="Last Name", width=300)
    
    # Date of Birth Picker
    def update_dob_field(e):
        dob_field.value = birth_date_picker.value.strftime("%Y-%m-%d")  # Format the date
        page.update()
    
    def pick_date(e):
        birth_date_picker.pick_date_dialog()  # Correct method to open the date picker
    
    birth_date_picker = ft.DatePicker(on_change=update_dob_field)
    dob_field = ft.TextField(label="Date of Birth", read_only=True, width=300)
    dob_picker_button = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=pick_date)
    dob_row = ft.Row([dob_field, dob_picker_button])
    
    message = ft.Text("", color="red")

    def save_profile(e):
        if first_name.value and last_name.value and dob_field.value:
            show_medical_mobility_page(username)  # Call the next page function
        else:
            message.value = "All fields must be filled."
            page.update()
    
    page.overlay.append(birth_date_picker)
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
