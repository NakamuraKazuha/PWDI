import flet as ft

def profile_setup_page(page, username, show_medical_mobility_page):
    """Profile setup screen UI with separated containers"""
    page.title = "Profile Information"
    page.bgcolor = "#EDF8ED"
    page.padding = 20
    
    # Background container
    background = ft.Container(
        content=ft.Image(
            src="assets/bgnew.jpg",
            fit=ft.ImageFit.FILL
        ),
        expand=True
    )
    
    # Title container
    title = ft.Container(
        content=ft.Text(
            "Profile Setup",
            text_align=ft.TextAlign.CENTER,
            color="#003B5B",
            size=24,
            weight=ft.FontWeight.BOLD,
        ),
        alignment=ft.alignment.center,
    )
    
    # Input fields
    first_name = ft.TextField(label="First Name", width=300)
    last_name = ft.TextField(label="Last Name", width=300)
    
    # Date of Birth Picker
    def update_dob_field(e):
        dob_field.value = birth_date_picker.value.strftime("%Y-%m-%d")
        page.update()
    
    def pick_date(e):
        birth_date_picker.pick_date_dialog()
    
    birth_date_picker = ft.DatePicker(on_change=update_dob_field)
    dob_field = ft.TextField(label="Date of Birth", read_only=True, width=300)
    dob_picker_button = ft.IconButton(icon=ft.icons.CALENDAR_MONTH, on_click=pick_date)
    
    dob_container = ft.Container(
        content=ft.Row([dob_field, dob_picker_button]),
        alignment=ft.alignment.center
    )
    
    # Error message container
    message = ft.Text("", color="red")
    
    # Save button
    def save_profile(e):
        if first_name.value and last_name.value and dob_field.value:
            show_medical_mobility_page(username)
        else:
            message.value = "All fields must be filled."
            page.update()
    
    save_button = ft.Container(
        content=ft.ElevatedButton(
            text="Save Profile",
            bgcolor="#006A8E",
            color="white",
            width=200,
            height=50,
            on_click=save_profile,
        ),
        alignment=ft.alignment.center,
    )
    
    page.overlay.append(birth_date_picker)
    page.update()
    
    # Input fields container
    input_fields = ft.Container(
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[first_name, last_name, dob_container, message],
        ),
        alignment=ft.alignment.center,
    )
    
    # Stack to combine everything
    return ft.Stack(
        controls=[background, title, input_fields, save_button],
        width=page.window.width,
        height=page.window.height,
    )
