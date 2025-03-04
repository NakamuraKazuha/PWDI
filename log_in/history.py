# pages/history.py
import flet as ft

def medical_history_page(page, username, show_legal_documentation_page):
    """Medical History Information page UI"""
    medical_history = ft.TextArea(label="Describe your medical history")
    message = ft.Text("", color="red")

    def next_click(e):
        if medical_history.value:
            show_legal_documentation_page(username)
        else:
            message.value = "Please provide your medical history."
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
                    "Medical History",
                    text_align=ft.TextAlign.CENTER,
                    color="#003B5B",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                ),
                medical_history,
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
