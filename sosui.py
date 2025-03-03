import flet as ft
from sosbackend import SOSHandler, send_sos, get_gps_location, cancel_sos
from plyer import vibrator

def vibrate_pattern():
    try:
        vibrator.vibrate(0.5)  # Vibrates for 500ms
    except NotImplementedError:
        print("Vibrating...")

def create_emergency_interface(page):
    countdown_label = ft.Text("", size=24, color="black", weight=ft.FontWeight.BOLD)  # Black text

    sos_handler = SOSHandler(send_sos, get_gps_location, cancel_sos, lambda: page.update())
    sos_handler.countdown_label = countdown_label  # Link UI label to backend

    # Top bar with only Home and Profile
    top_bar = ft.Container(
        padding=ft.padding.only(left=20, right=20, top=10),
        content=ft.Row(
            [
                ft.IconButton(icon=ft.icons.HOME, icon_color="#004d40", icon_size=30),
                ft.Container(expand=1),  # Spacer to push profile icon to the right
                ft.IconButton(icon=ft.icons.ACCOUNT_CIRCLE, icon_color="#004d40", icon_size=30),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            width=400,
        )
    )

    # Function to create outer circle layers
    def sos_button_content(bg_color, size):
        return ft.Container(
            width=size,
            height=size,
            bgcolor=bg_color,
            border_radius=1000,
            alignment=ft.alignment.center,
        )

    # Main SOS button
    sos_main_button = ft.Container(
        width=250,
        height=250,
        bgcolor="#db3a34",  # Main red SOS button
        border_radius=1000,
        alignment=ft.alignment.center,
        content=ft.Text("SOS", color="white", size=40, weight=ft.FontWeight.BOLD),
    )

    # SOS Button with perfect center alignment
    sos_button = ft.Container(
        alignment=ft.alignment.center,
        content=ft.Stack(
            [
                sos_button_content("#f28b82", 290),  # Light red outer layer
                sos_button_content("#e53935", 270),  # Medium red middle layer
                sos_main_button  # Main red button
            ],
            alignment=ft.alignment.center  # Ensures everything stays centered
        )
    )

    # Functionality to change button color on press
    def start_sos_action():
        sos_main_button.bgcolor = "#b71c1c"  # Darker red when pressed
        sos_handler.start_countdown()
        vibrate_pattern()  # Trigger vibration
        page.update()

    def cancel_sos_action():
        sos_main_button.bgcolor = "#db3a34"  # Reset color
        sos_handler.cancel_countdown()
        page.update()

    # Make SOS button responsive
    sos_button_interactive = ft.GestureDetector(
        content=sos_button,
        on_tap_down=lambda e: start_sos_action(),
        on_tap_up=lambda e: cancel_sos_action(),
    )

    # Cancel button (orange)
    cancel_button = ft.IconButton(
        icon=ft.icons.CANCEL,
        icon_color="orange",
        icon_size=50,
        on_click=lambda e: sos_handler.cancel_sos_action(),
    )

    # Emergency UI layout
    emergency_container = ft.Stack(
        [
            ft.Image(src="bgnew.jpg", width=440, height=956, fit=ft.ImageFit.COVER),  # Background Image
            ft.Column(
                [
                    top_bar,
                    ft.Container(expand=80),  # Spacer to push SOS button down
                    sos_button_interactive,
                    countdown_label,  # Countdown text
                    cancel_button,
                    ft.Container(expand=1),  # Bottom padding
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
            ),
        ]
    )

    return emergency_container

def main(page: ft.Page):
    page.title = "SOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False
    page.add(create_emergency_interface(page))

ft.app(target=main)