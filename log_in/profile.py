import flet as ft

def consent_page(page, username, show_profile_setup):
    """Consent screen UI"""
    
    consent_checkbox = ft.Checkbox(
        label="I consent to the terms and conditions.",
        label_style=ft.TextStyle(color="#003B5B")
    )

    message = ft.Text("", color="red")

    def next_click(e):
        if consent_checkbox.value:
            show_profile_setup(username)  # Pass username to the profile setup page
        else:
            message.value = "You must consent to the terms and conditions."
            message.color = "red"
            page.update()

    return ft.Container(
        width=page.width,
        height=page.height,
        bgcolor="#F0FAEF",
        border_radius=10,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,  # Center vertically
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Center horizontally
            controls=[
                ft.Text(
                    "Consent",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Please read and accept our terms and conditions.",
                    text_align=ft.TextAlign.CENTER,
                    size=15,
                    color="#003B5B"
                ),
                ft.Row(  # Wrap checkbox in Row to center it perfectly
                    controls=[consent_checkbox],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Container(
                    content=message,
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    content=ft.ElevatedButton(
                        text="Next",
                        bgcolor="#003B5B",
                        color="white",
                        width=200,
                        height=50,
                        on_click=next_click,
                    ),
                    alignment=ft.alignment.center
                ),
            ],
        ),
    )
