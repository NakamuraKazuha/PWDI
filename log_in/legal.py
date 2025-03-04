# pages/legal.py
import flet as ft

def legal_documentation_page(page, username):
    """Legal and Documentation page UI"""
    legal_terms_checkbox = ft.Checkbox(label="I agree to the legal terms and conditions.")
    message = ft.Text("", color="red")

    def submit_click(e):
        if legal_terms_checkbox.value:
            # Simulate the final submission of the form
            message.value = "All steps completed. Thank you for your submission!"
            message.color = "green"
            page.update()
        else:
            message.value = "You must agree to the legal terms."
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
                    "Legal & Documentation",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Please read and accept the legal terms before submitting.",
                    text_align=ft.TextAlign.CENTER,
                    size=18,
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
    )
