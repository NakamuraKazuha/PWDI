
from flet import *
from first_interface import create_ui
from flet import app
from splash import splash_screen

from profile_page import create_profile_ui

import os
def main(page: Page): 
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False

    page.fonts = {
        "lalezar": "fonts/Lalezar-Regular.ttf", #font
    }


    page.update()

    page.clean()
    page.add(create_ui(page))

    
app(target=main, assets_dir="assets")

