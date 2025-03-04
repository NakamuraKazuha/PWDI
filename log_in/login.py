from flet import *
from navigation import authenticate_user

def login_page(page, show_signup, show_consent_page):
    """Login screen UI with separated containers"""

    # Background container
    background = Container(
        content=Image(
            src="assets/bgnew.jpg",
            fit=ImageFit.FILL
        ),
        expand=True
    )

    logo = Container(
        content=Image(src="assets/logo1.png", width=150, height=150),
        left=10,
        right=10,
        top=20
    )

    # Title container
    title =  Container(
        content= Text(
            "Log In",
            text_align= TextAlign.CENTER,
            color="#003B5B",
            size=24,
            weight= FontWeight.BOLD,
        ),
        top=200,  
        left=0,
        right=0,
        alignment= alignment.center
    )
    
    # Username and password fields
    username = Container(
    content=TextField(
        label="Enter Username",
        text_style=TextStyle(color="#003B5B", font_family="Lalezar"),  # Text inside the field
        label_style=TextStyle(color="#003B5B"),  # Label color
        bgcolor="#F0FAEF",  # Background color
        border=InputBorder.NONE  # Remove border
    ),
    border_radius=8,  # Adjust the corner radius as needed
)
    password = Container(
    content=TextField(
    label="Password",
    password=True,
    text_style=TextStyle(color="#003B5B", font_family="lalezar"),  
    label_style=TextStyle(color="#003B5B"),
    bgcolor="#F0FAEF",
    border=InputBorder.NONE,  
        ),
    border_radius=8,
    )
    message =  Text("", color="red")
    
    #user name text
    username_text= Container(
    content=Text(
        value="User Name",  
        size=17,
        weight=FontWeight.BOLD,
        color="#003B5B",
        font_family="Lalezar",
    ),
    left=20,
    top=303
    )

    password_text= Container(
    content=Text(
        value="Password",  
        size=17,
        weight=FontWeight.BOLD,
        color="#003B5B",
        font_family="Lalezar",
    ),
    left=20,
    top=393
    )

    # Login button
    def login_click(e):
        success, msg = authenticate_user(username.value, password.value)
        message.value = msg
        message.color = "green" if success else "red"
        page.update()
        if success:
            show_consent_page(username.value)  # Pass the username to the consent page

    login_button = Container(
    content=ElevatedButton(
        text="Log In",
        bgcolor="#003B5B",
        color="white",
        width=200,
        height=50,
        on_click=login_click,
        style=ButtonStyle(
            shape=RoundedRectangleBorder(radius=8)  # Change the radius as needed
        ),
    ),
    top=490,  # Adjust position
    left=0,
    right=0,
    alignment=alignment.center
)


    # Sign-up link
    signup_link = Container(
    content=TextButton(
        "New to PWDI? Sign Up",
        on_click=lambda e: show_signup(),
        style=ButtonStyle(color="#003B5B")  # Change to desired color
    ),
    top=570,
    left=0,
    right=0,
    alignment=alignment.center
)
    # Input fields container
    input_fields = Container(
    content=Column(
        alignment=MainAxisAlignment.CENTER,
        horizontal_alignment=CrossAxisAlignment.CENTER,
        spacing=40,  
        controls=[username, password, message],
    ),
    top=335,  
    left=50,
    right=50,
)


    # Combine everything into a Stack
    return  Stack(
        controls=[background, logo, username_text, password_text, title, input_fields, login_button, signup_link],
        width=page.window.width,
        height=page.window.height
    )
