from flet import *

from commands import emergency_button, share_button, home_button, profile, notif

def create_ui(page: Page):

    background = Container(
        content=Image(
            src="bgnew.jpg",
            fit=ImageFit.FILL
        ),
        expand=True 
    )

    button_size = 250
    circle_des1 = button_size + 18
    circle_des2 = button_size + 35

    home_icon = Container(
        content=IconButton(
            icon=icons.HOME,
            icon_size=40,
            icon_color="#085F61",
            on_click=home_button
        ),
        left=20,
        top=100
    )

    profile_icon = Container(
        content=IconButton(
            icon=icons.PERSON, 
            icon_size=40,
            icon_color="#085F61",
            on_click=profile
        ),
        right=20,
        top=100
    )

    notif_icon = Container(
        content=IconButton(
            icon=icons.NOTIFICATIONS,
            icon_size=35,
            icon_color="#085F61",
            on_click=notif
        ),
        right=60,
        top=103
    )

    share_icon = Container(
        content=IconButton(
            icon=icons.SHARE,
            icon_size=50,
            icon_color="#085F61"
        ),
        left=120,
        top=598
    )

    # Circle Design
    circle_design1 = Container(
        width=circle_des1,
        height=circle_des1,
        bgcolor="#DB3A34",
        border_radius=1000,
        alignment=alignment.center,
        left=(425 - circle_des1) / 2,
        top=200
    )

    circle_design2 = Container(
        width=circle_des2,
        height=circle_des2,
        bgcolor="#C5B7B7",
        border_radius=1000,
        alignment=alignment.center,
        left=(425 - circle_des2) / 2,
        top=193
    )

    # Emergency Button
    btn = Container(
        content=ElevatedButton(
            text="EMERGENCY",
            on_click=emergency_button,
            bgcolor="#D40032",
            color="#F0FAEF",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=1000),
                padding=15,
                elevation=5,
                text_style=TextStyle(
                    size=37,
                    weight=FontWeight.BOLD,
                    font_family="Lalezar"
                )
            ),
            width=button_size,
            height=button_size
        ),
        left=(425 - button_size) / 2,
        top=210,
        width=button_size,
        height=button_size
    )

    # Share Button
    share_btn = Container(
        content=ElevatedButton(
            text="     SHARE",
            on_click=share_button,
            bgcolor="#F0FAEF",
            color="#085F61",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=12),
                padding=10,
                elevation=5,
                text_style=TextStyle(
                    size=30,
                    weight=FontWeight.BOLD,
                    font_family="Lalezar"
                )
            ),
            width=270,
            height=60
        ),
        left=30,
        right=30,
        top=600
    )

    share_des = Container(
        width=300,
        height=5,
        bgcolor="#F0FAEF",
        border_radius=10,
        alignment=alignment.center,
        left=50,
        top=665
    )

    return Stack(
        controls=[
            background, 
            home_icon, 
            profile_icon,
            notif_icon,
            circle_design2,
            circle_design1,
            btn,
            share_btn,
            share_icon,
            share_des
        ],
        width=page.window.width,
        height=page.window.height
    
    )
