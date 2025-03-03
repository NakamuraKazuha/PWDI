from flet import *


def create_profile_ui(page: Page):

    bg = Container(
        content=Image(src="bgnew.jpg", fit=ImageFit.FILL),
        expand=True
    )

    logo = Container(
        content=Image(src="logo1.png", width=100, height=90),
        left=5, top=5
    )

    home_icon = Container(
        content=IconButton(
            icon=icons.HOME, icon_size=40, icon_color="#085F61",
            on_click=lambda e: go_back(e, page)
        ),
        left=20, top=110
    )

    #uI

    title = Container(
    content=Text(
        value="Profile Information",  
        size=25,
        weight=FontWeight.BOLD,
        color="#003B5B",
        font_family="Lalezar",
        text_align=TextAlign.CENTER,
    ),
    left=50,
    right=50,
    top=165
    )
#User ID - label
    user = Container(
    content=Text(
        value="User ID", 
        size =20, 
        weight=FontWeight.BOLD,
        color="#003B5B",
        font_family="Lalezar",
        text_align=TextAlign.CENTER
    ),
    left=20,
    top=215
    )
#User ID Container
    id_cont = Container(
            bgcolor="#F0FAEF", 
            padding=5,
            border_radius=5,
            width=350,
            height=40,
            alignment=alignment.center_left,
            left=20,
            top=250,
            border=border.all(1, "#084C61")
    )
#Personal Details - Label
    personal = Container(
    content=Text(
        value="Personal Details", 
        size =20, 
        weight=FontWeight.BOLD,
        font_family="lalezar",
        color="#003B5B",
        text_align=TextAlign.CENTER
    ),
    left=20,
    top=300
    )
#Full Name Container
    full_name = Container(
        content=Text("Full Name: ",
                     size=12,
                     weight=FontWeight.BOLD,
                     color="#ABC6C5",
                     text_align=TextAlign.LEFT
                     ), 
            bgcolor="#F0FAEF", 
            padding=5,
            border_radius=5,
            width=350,
            height=30,
            alignment=alignment.center_left,
            left=20,
            top=330
    )
#Birthday Container
    birthday = Container(
        content=Text("Date of Birth: ",
                     size=12,
                     weight=FontWeight.BOLD,
                     color="#ABC6C5",
                     text_align=TextAlign.LEFT
                     ), 
            bgcolor="#F0FAEF", 
            padding=5,
            border_radius=5,
            width=350,
            height=30,
            alignment=alignment.center_left,
            left=20,
            top=370
    )
#Gender Container
    gender = Container(
        content=Text("Gender: ",
                     size=12,
                     weight=FontWeight.BOLD,
                     color="#ABC6C5",
                     text_align=TextAlign.LEFT
                     ), 
            bgcolor="#F0FAEF", 
            padding=5,
            border_radius=5,
            width=350,
            height=30,
            alignment=alignment.center_left,
            left=20,
            top=410
    )
 #Contact Container    
    contact = Container(
        content=Text("Contact Number: ",
                     size=12,
                     weight=FontWeight.BOLD,
                     color="#ABC6C5",
                     text_align=TextAlign.LEFT
                     ), 
            bgcolor="#F0FAEF", 
            padding=5,
            border_radius=5,
            width=350,
            height=30,
            alignment=alignment.center_left,
            left=20,
            top=450
    )
#Address Container
    address = Container(
        content=Text("Current Address: ",
                     size=12,
                     weight=FontWeight.BOLD,
                     color="#ABC6C5",
                     text_align=TextAlign.LEFT
                     ), 
            bgcolor="#F0FAEF", 
            padding=5,
            border_radius=5,
            width=350,
            height=30,
            alignment=alignment.center_left,
            left=20,
            top=490
    )

    #More information- Label
    more_info = Container(
    content=Text(
        value="More Information", 
        size =20, 
        weight=FontWeight.BOLD,
        color="#003B5B",
        font_family="lalezar",
        text_align=TextAlign.CENTER
    ),
    left=20,
    top=550
    )

#Buttons for Nore Information
    #Medical and Mobility information
    medical_info = Container(
    content=ElevatedButton(
        content=Row(
            controls=[
                Text("Medical and Mobility Information",
                    size=15, 
                    weight=FontWeight.BOLD, 
                    font_family="Lalezar"
                )
            ],
            alignment=MainAxisAlignment.START 
        ),
        on_click=lambda e: import_medical(e),  
        bgcolor="#F0FAEF",
        color="#085F61",
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=12),
            padding=padding.only(left=10),  
            elevation=5
        ),
        width=250,
        height=40
    ),
    left=30,
    right=30,
    top=580
)


    #Medical History
    medical_histo = Container(
    content=ElevatedButton(
        content=Row(
            controls=[
                Text("Medical History", 
                    size=15, 
                    weight=FontWeight.BOLD, 
                    font_family="Lalezar"
                )
            ],
            alignment=MainAxisAlignment.START  
        ),
        on_click=lambda e: import_medical_histo(e),
        bgcolor="#F0FAEF",
        color="#085F61",
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=12),
            padding=padding.only(left=10),
            elevation=5
        ),
        width=200,  
        height=40
    ),
    left=30,
    right=30,
    top=630
)


    #Legal & Documentation
    legal = Container(
    content=ElevatedButton(
        content=Row(
            controls=[
                Text("Legal & Documentation",
                    size=15, 
                    weight=FontWeight.BOLD, 
                    font_family="Lalezar"
                )
            ],
            alignment=MainAxisAlignment.START  # Left-align text
        ),
        on_click=lambda e: import_medical_histo(e),  
        bgcolor="#F0FAEF",
        color="#085F61",
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=12),
            padding=padding.only(left=10),  
            elevation=5
        ),
        width=200,  
        height=40
    ),
    left=30,
    right=30,
    top=680
)

    #Edit Profile
    edit = Container(
        content=ElevatedButton(
            text="Edit profile",
            on_click=lambda e: import_edit(e),  
            bgcolor="#ABC6C5",
            color="#EDF8ED",
            style=ButtonStyle(
                shape=RoundedRectangleBorder(radius=5),
                padding=10,
                elevation=5,
                text_style=TextStyle(size=13, weight=FontWeight.BOLD, font_family="Lalezar")
            ),
            width=10,
            height=25
        ),
        left=150,
        right=150,
        top=730
    )

    return Stack(
        [
            bg, 
            home_icon, 
            logo, 
            title,
            user,
            personal,
            full_name,
            birthday,
            gender,
            contact,
            address,
            id_cont,

            more_info,

            medical_info,
            medical_histo,
            legal,
            edit,
            


        ]
        )

def import_medical(e):
    from commands import medical
    medical(e)

def import_medical_histo(e):
    from commands import medical_history
    medical_history(e)

def import_legal(e):
    from commands import legal_docu
    legal_docu(e)

def import_edit(e):
    from commands import edit_profile
    edit_profile(e)


def go_back(e, page):
    from first_interface import create_ui  # Import dynamically
    page.clean()
    page.add(create_ui(page))
    page.update()
