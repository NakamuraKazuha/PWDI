from flet import *
import time
import threading

def splash_screen(page: Page, on_splash_end):
    """Displays the splash screen before transitioning to the main UI."""
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False

    # Background image (Full Screen)
    splash_background = Container(
        content=Image(
            src="bgnew.jpg",  # Make sure this image exists
            fit=ImageFit.COVER  # Cover the entire screen
        ),
        expand=True
    )

    # Logo Image (Centered + Animated)
    logo = Container(
        content=Image(
            src="logo1.png",  # Ensure this image exists
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

    # Function to transition from splash to welcome page
    def go_to_welcome():
        time.sleep(3)  # Pause for 3 seconds
        page.clean()  # Clear splash screen
        on_splash_end()  # Call the callback to navigate to the welcome page
        page.update()

    threading.Thread(target=go_to_welcome, daemon=True).start()
