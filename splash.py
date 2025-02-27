from flet import *
import time
import threading
from first_interface import create_ui

def splash_screen(page: Page):
    """Displays the splash screen before transitioning to the main UI."""
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False

    # Background image (Full Screen)
    splash_background = Container(
        content=Image(
            src="bgnew.jpg",  # image
            fit=ImageFit.COVER  #scale
        ),
        expand=True
    )

    #Logo properties
    logo = Container(
        content=Image(
            src="logo1.png",  # Ensure this image exists - assets
            fit=ImageFit.CONTAIN  # Keep original proportions
        ),
        width=200,  # Adjust as needed
        height=200,
        top=280,
        left=100,
        opacity=0,  # Start invisible
        animate_opacity=1000  # Fade-in effect in 1 second
    )

    # Stack all elements (Background first, then logo)
    page.add(
        Stack(
            controls=[splash_background, logo],  
            width=page.window.width,
            height=page.window.height
        )
    )

    page.update()

    # Animate the logo
    logo.opacity = 1  # Make the logo visible
    page.update()

    # Function to transition from splash to main UI
    def go_to_main():
        time.sleep(3)  # Pause for 3 seconds
        page.clean()  # Clear splash screen
        page.add(create_ui(page))  # Load main UI
        page.update()

    threading.Thread(target=go_to_main, daemon=True).start()

# Run the app
app(target=splash_screen)
