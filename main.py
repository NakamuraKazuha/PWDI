from flet import *
from commands import emergency_button, share_button, home_button, profile, notif
from first_interface import create_ui
from flet import app
from splash import splash_screen



def main(page: Page):
  def main(page: Page):
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False

    page.clean() 
    page.add(create_ui(page))  

app(target=main)

