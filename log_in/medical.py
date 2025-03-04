# pages/medical.py
import flet as ft

def medical_mobility_page(page, username, show_medical_history_page):
    """Medical and Mobility Information page UI"""
    medical_condition = ft.TextField(label="Medical Condition (if any)")
    mobility_issue = ft.TextField(label="Mobility Issues (if any)")
    message = ft.Text("", color="red")

    def next_click(e):
        # Simulate saving the medical and mobility information
        if medical_condition.value or mobility_issue.value:
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
