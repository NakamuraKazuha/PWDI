import flet as ft
from sosbackend import SOSHandler, get_gps_location, cancel_sos
from plyer import vibrator
import asyncio
import websockets
import json

# Global variable to track if data was sent
data_sent = False

async def send_sos():
    """Sends an SOS message via WebSocket."""
    global data_sent
    uri = "ws://localhost:6789"  # WebSocket Server Address
    try:
        async with websockets.connect(uri) as websocket:
            patient_info = {
                "full_name": "Gayle Dy",
                "location": get_gps_location(),
                "dob": "1990-05-15",
                "gender": "Female",
                "contact_number": "1234567890",
                "current_address": "123 Bulacao Cebu City",
                "emergency_contact": {
                    "name": "Shane Marie Dy",
                    "relationship": "Sister",
                    "contact_number": "0987654321"
                },
                "disability_type": "Physical",
                "severity_level": "Moderate",
                "assistive_devices": "Wheelchair",
                "communication_prefs": "Phone Call",
                "mobility_needs": "Uses Wheelchair",
                "needs_help": True
            }
            await websocket.send(json.dumps(patient_info))
            print("SOS Sent! Notifying emergency contacts via web.")
            data_sent = True
    except Exception as e:
        print(f"Error sending SOS: {e}")

# Function to send data via WebSockets on button click
def send_data(e):
    global data_sent
    if not data_sent:
        asyncio.create_task(send_sos())  # ✅ Run the async function properly

# Vibrator function for mobile
def vibrate_pattern():
    try:
        vibrator.vibrate(0.5)
    except NotImplementedError:
        print("Vibrating...")

# UI creation function
def create_emergency_interface(page):
    countdown_label = ft.Text("", size=24, color="black", weight=ft.FontWeight.BOLD)
    sos_handler = SOSHandler(send_sos, get_gps_location, cancel_sos, lambda: page.update())
    sos_handler.countdown_label = countdown_label

    top_bar = ft.Container(
        padding=ft.padding.only(left=20, right=20, top=10),
        content=ft.Row(
            [
                ft.IconButton(icon=ft.icons.HOME, icon_color="#004d40", icon_size=30),
                ft.Container(expand=1),
                ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, icon_color="#004d40", icon_size=30),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=400,
        )
    )

    def sos_button_content(bg_color, size):
        return ft.Container(
            width=size,
            height=size,
            bgcolor=bg_color,
            border_radius=1000,
            alignment=ft.alignment.center,
        )

    sos_main_button = ft.Container(
        width=250,
        height=250,
        bgcolor="#db3a34",
        border_radius=1000,
        alignment=ft.alignment.center,
        content=ft.Text("SOS", color="white", size=40, weight=ft.FontWeight.BOLD),
    )

    sos_button = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Stack(
            [
                sos_button_content("#f28b82", 290),
                sos_button_content("#e53935", 270),
                sos_main_button
            ],
            alignment=ft.alignment.center
        )
    )

    def start_sos_action():
        sos_main_button.bgcolor = "#b71c1c"
        sos_handler.start_countdown()
        vibrate_pattern()
        page.update()

    def cancel_sos_action():
        sos_main_button.bgcolor = "#db3a34"
        sos_handler.cancel_countdown()
        page.update()

    sos_button_interactive = ft.GestureDetector(
        content=sos_button,
        on_tap_down=lambda e: start_sos_action(),
        on_tap_up=lambda e: cancel_sos_action(),
    )

    cancel_button = ft.IconButton(
        icon=ft.icons.CANCEL,
        icon_color="orange",
        icon_size=50,
        on_click=lambda e: sos_handler.cancel_sos_action(),
    )

    emergency_container = ft.Stack(
        [
            ft.Image(src="bgnew.jpg", width=440, height=956, fit=ft.ImageFit.COVER),
            ft.Column(
                [
                    top_bar,
                    ft.Container(expand=80),
                    sos_button_interactive,
                    countdown_label,
                    cancel_button,
                    ft.Container(expand=1),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
            ),
        ]
    )

    return emergency_container

# Main Flet application
def main(page: ft.Page):
    page.title = "SOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False
    page.add(create_emergency_interface(page))
    btn = ft.ElevatedButton("SOS", on_click=send_data)
    page.add(btn)

ft.app(target=main)
