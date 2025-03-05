# share.py
import flet as ft
from database import fetch_acc_users, remove_acc_user, fetch_auth_viewers, fetch_notifications, remove_auth_viewer, session, Notification, AuthorizedViewers, Users
from functools import partial

def share(page: ft.Page):
    # Your existing share page implementation
    # Ensure it returns a UI component (e.g., a Container or Column)

    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 440
    page.window.height = 956
    page.window.resizable = False 

    # Colors
    gradient_bg = ["#F0FAEF", "#084C61"]
    icon_colors = "#084C61"
    box_colors = "#F0FAEF"

    accessible_users_column = ft.Column(
        scroll="auto"
    )

    def remove_accessible_user(e, user_id, owner_id):
        remove_acc_user(owner_id, user_id) 
        rebuild_acc_users_ui(owner_id)  


    def rebuild_acc_users_ui(viewer_id): 
        accessible_users_column.controls.clear()

        accessible_users = fetch_acc_users(viewer_id)  # viewer_id to get accessible users

        for user_id, user_name in accessible_users:
            accessible_users_column.controls.append(
                ft.Container(
                    bgcolor=box_colors, height=45, width=400,
                    border_radius=5,
                    padding=ft.padding.only(top=5, left=20, right=5, bottom=5),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(user_name, size=20),
                            ft.IconButton(
                                ft.icons.CLOSE,
                                padding=ft.padding.only(top=5, bottom=5),
                                icon_size=25,
                                icon_color=icon_colors,
                                on_click=partial(remove_accessible_user, user_id=user_id, owner_id=viewer_id)
                            )
                        ]
                    )
                )
            )

        page.update()  # Ensure the UI updates after removal


    # Wrap it in a scrollable container 
    scrollable_accessible_users_container = ft.Container(
        height=270,  # i have no idea how to make this dynamic
        content=accessible_users_column
    )

    #for people that can get notified sa imo emergencies 
    authorized_viewers_column = ft.Column (
        scroll = "auto"
    )

    def remove_authorized_viewer(e, owner_id, viewer_id):
        remove_auth_viewer(owner_id, viewer_id)  #pass both ids to remove the viewer
        rebuild_auth_viewers_ui(owner_id)  # refresh UI to show updated list

    def rebuild_auth_viewers_ui(owner_id):
        authorized_viewers_column.controls.clear()  #it clears UI to reload 

        authorized_viewers = fetch_auth_viewers(owner_id)  #

        for viewer_id in authorized_viewers:
            viewer_name = session.query(Users.name).filter_by(user_id=viewer_id).scalar()  
            authorized_viewers_column.controls.append(
                ft.Container(
                    bgcolor=box_colors, height=45, width=400,
                    border_radius=5,
                    padding=ft.padding.only(top=5, left=20, right=5, bottom=5),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(viewer_name, size=20),
                            ft.IconButton(
                                ft.icons.CLOSE,
                                padding=ft.padding.only(top=5, bottom=5),
                                icon_size=25,
                                icon_color=icon_colors,
                                on_click=partial(remove_authorized_viewer, owner_id=owner_id, viewer_id=viewer_id) 
                            )
                        ]
                    )
                )
            )

        page.update()  

    scrollable_authorized_viewers_container = ft.Container(
        height=270, #270 fits the boxes perfectly, bale 5 ka tao iya makita sa scroll
        content=authorized_viewers_column
    )
    
    def handle_search_submit(e, viewer_id):
        query = (e.control.value.strip().lower() if e and hasattr(e, "control") and e.control else "").lower()
        is_searching = bool(query)  #if naa ang term

        # Accessible users
        user_entries = []
        for user_id, user_name in fetch_acc_users(viewer_id):
            color = "#A8DADC" if is_searching and query in user_name.lower() else box_colors  #this does the highlights
            user_entries.append((user_name, user_id, color))

        user_entries.sort(key=lambda x: (x[2] != "#A8DADC", x[0]))  # this is the sort: highlights first, then sort

        accessible_users_column.controls = [
            ft.Container(
                bgcolor=color, height=45, width=400,
                border_radius=5,
                padding=ft.padding.only(top=5, left=20, right=5, bottom=5),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(user_name, size=20),
                        ft.IconButton(
                            ft.icons.CLOSE,
                            padding=ft.padding.only(top=5, bottom=5),
                            icon_size=25,
                            icon_color=icon_colors,
                            on_click=partial(remove_accessible_user, user_id=user_id, owner_id=viewer_id)
                        )
                    ]
                )
            ) for user_name, user_id, color in user_entries
        ]

        # Authorized viewers
        auth_entries = []
        auth_viewers = fetch_auth_viewers(viewer_id)

        if isinstance(auth_viewers, list):
            for auth_id in auth_viewers:
                viewer_name = session.query(Users.name).filter_by(user_id=auth_id).scalar()
                if viewer_name:
                    color = "#A8DADC" if is_searching and query in viewer_name.lower() else box_colors
                    auth_entries.append((viewer_name, auth_id, color))

        auth_entries.sort(key=lambda x: (x[2] != "#A8DADC", x[0])) 

        authorized_viewers_column.controls = [
            ft.Container(
                bgcolor=color, height=45, width=400,
                border_radius=5,
                padding=ft.padding.only(top=5, left=20, right=5, bottom=5),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(viewer_name, size=20),
                        ft.IconButton(
                            ft.icons.CLOSE,
                            padding=ft.padding.only(top=5, bottom=5),
                            icon_size=25,
                            icon_color=icon_colors,
                            on_click=partial(remove_authorized_viewer, owner_id=viewer_id, viewer_id=auth_id)
                        )
                    ]
                )
            ) for viewer_name, auth_id, color in auth_entries
        ]

        page.update() 


    #the search open bar thingy
    search = ft.SearchBar(
        height= 40,
        width = 200,

        #style of the texts sa search
        bar_hint_text="Search for User",
        bar_hint_text_style=ft.TextStyle(size=14, color="#C9D7C7"),
        bar_text_style=ft.TextStyle(size=14, color="black"),

        #the style of the search bar
        bar_bgcolor="#E1EEE6",
        bar_shadow_color="#749EA3",

        #actions
        on_submit=lambda e:handle_search_submit(e, viewer_id),
        
        #make the default search bar invisible 
        visible=False
    )

    def toggle_search_bar(e):
        search.visible = not search.visible  # Toggle visibility first

        if not search.visible:  # If its being closed
            search.value = ""  #clears the search
            handle_search_submit(ft.Control(), viewer_id) #if i mu close, then reloads the boxes normally

        page.update()  # Refresh the UI


    def handle_submitID(e):
        entered_id = e.control.value.strip()
        if entered_id.isdigit():  # Only accepts digits
            user_id = int(entered_id)

            # Check if the user exists in the Users table
            user = session.query(Users).filter_by(user_id=user_id).first()
            if user:
                # Check if the user is already in AuthorizedViewers instead of AccessibleUser
                if not session.query(AuthorizedViewers).filter_by(viewer_id=user_id, owner_id=viewer_id).first():
                    session.add(AuthorizedViewers(viewer_id=user_id, owner_id=viewer_id))  
                    session.commit()

                    viewer = session.query(Users).filter_by(user_id=viewer_id).first()
                    viewer_name = viewer.name

                    #this here sends the message
                    notification_message = f"{viewer_name} added you."
                    new_notification = Notification(user_id=user_id, message=notification_message)
                    session.add(new_notification)
                    session.commit()

                    rebuild_auth_viewers_ui(viewer_id)  # Refresh UI for authorized viewers
                    rebuild_notifications_ui(user_id)
                else:
                    print(f"ID {user_id} is already in Authorized Viewers.")
            else:
                print(f"Error: User ID {user_id} does not exist in Users.")
        else:
            print("Error: ID must contain only numbers!")

    # Content sa page 
    share_contents = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    controls=[
                        ft.Container(
                            content=ft.IconButton(
                                ft.icons.HOME,
                                icon_size=30,
                                icon_color=icon_colors,
                                on_click=lambda e: print("Home clicked!")
                            )
                        ),
                        ft.Row(
                            controls=[
                                search,
                                ft.Container(
                                    content=ft.IconButton(
                                        ft.icons.SEARCH,
                                        icon_size=30,
                                        icon_color=icon_colors,
                                        on_click=toggle_search_bar
                                    )
                                ),
                                ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.IconButton(
                                                ft.icons.NOTIFICATIONS,
                                                icon_size=30,
                                                icon_color=icon_colors,
                                                on_click=lambda e: toggle_notifications(True) #i still dont get why this needs to specify lambda
                                            )
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                ),
                
                ft.Container (height = 10), #add space
                

                #for share my records
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    controls=[
                        ft.Text(value='Share My Records:', style=ft.TextStyle(size=18,font_family="Cocogoose")),
                        ft.Container(
                            width=150,  
                            content=ft.TextField(
                            label="ID Number", 
                            label_style=ft.TextStyle(size= 15,color = "#C9D7C7", weight=ft.FontWeight.BOLD),
                            border_radius=20,
                            border_color="#9B1B30", 
                            text_style=ft.TextStyle(size=14, color="black"),  
                            on_submit=handle_submitID
                            ),
                        ),
                    ]
                ),
                
                ft.Container (height =10),
                ft.Text(value = 'Accessible Users', style=ft.TextStyle(size=18,font_family="Cocogoose") ),
                ft.Container(
                    padding = ft.padding.only(top = 5, bottom =10),
                    content = scrollable_accessible_users_container
                ),

                ft.Container (height =10),
                ft.Text(value = 'Authorized Viewers:', style=ft.TextStyle(size=18,font_family="Cocogoose")),
                ft.Container(
                    padding = ft.padding.only(top = 5, bottom =10),
                    content = scrollable_authorized_viewers_container
                ),
            ]
        )
    )

    # Border container 
    border = ft.Container(
        expand=True,
        border_radius=35,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=gradient_bg  
        ),
        padding=ft.padding.only(
            top=20, left=20, right=20, bottom=5
        ),
        content=share_contents  
    )

    # Main container 
    container = ft.Container(
        expand=True,
        border_radius=35,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_center,
            end=ft.alignment.bottom_center,
            colors=gradient_bg  
        ),
        content=border,
        animate=ft.animation.Animation(300,ft.AnimationCurve.EASE_IN_OUT)
    )

    # Ask for the user ID!!!!! NOTE: TO DELETE ONCE NAA NA KA MELOOO
    viewer_id = input("Enter your 6-digit User ID to check accessible users: ").strip()
    if not (viewer_id.isdigit() and len(viewer_id) == 6):
        print("Invalid ID. Must be a 6-digit number.")
        return  # Exit if the input is invalid

    viewer_id = int(viewer_id)  # Convert to integer for database queries
    rebuild_auth_viewers_ui(viewer_id)  
    rebuild_acc_users_ui(viewer_id)

    #initializing
    notification_controls = [] 
    notification_list = ft.ListView() 

    def rebuild_notifications_ui(viewer_id):
        notifications = fetch_notifications(viewer_id)

        notification_controls.clear()  #clear prev notifs

        for notif in notifications:
            message = notif[1] if isinstance(notif, tuple) else notif  # Handle tuple or string

            icon = ft.Icon(ft.icons.NOTIFICATIONS, color="orange", size=20)

            notif_text = ft.Text(
                message, 
                size=14, 
                weight=ft.FontWeight.NORMAL, 
                width=None, 
                text_align=ft.TextAlign.LEFT,
            )

            notif_card = ft.Container(
                padding=10,
                bgcolor="#FFFFFF",
                border_radius=10,
                shadow=ft.BoxShadow(blur_radius=4, spread_radius=1, color="#CCCCCC"),
                content=ft.Row(
                    [
                        icon,
                        ft.Container(content=notif_text, expand=True)  
                    ], 
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10, 
                ),
                width=notif_panel.width * 0.9, 
            )

            notification_controls.append(notif_card)
            notification_controls.append(ft.Container(height=5))

        notification_list.controls = notification_controls
        notification_list.update()

    notif_panel = ft.Container(
        width=-5, 
        height=page.window.height,
        bgcolor="#F0FAEF",
        border_radius=35,
        padding=15,
        content=ft.Column(controls=[ft.Text("Notifications", size=20, weight=ft.FontWeight.BOLD), notification_list]),
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT)
    )

    # state sa toggle notifs
    is_notif_open = [False]
    def toggle_notifications(e):
        is_notif_open[0] = not is_notif_open[0] 
        
        #if i open ang notifications, it hides the search bar
        if is_notif_open[0]:  
            search.visible = False  #Hide search bar
            search.value = ""  #clears the search
            rebuild_notifications_ui(viewer_id)
            rebuild_acc_users_ui(viewer_id)  # Ensure accessible users stay
            rebuild_auth_viewers_ui(viewer_id)  # Ensure authorized viewers stay
        
        notif_panel.width = page.width * 0.4 if is_notif_open[0] else 0  # Show/hide notifications
        page.update()

    # add the pages
    page.add(ft.Row([container, notif_panel], expand=True, spacing=0)) #samok the spacing diay thats why it has extra space
    page.update()


    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("This is the Share Page", size=30, color="black"),
                ft.ElevatedButton(
                    "Go Back",
                    on_click=lambda e: page.go("/")  # Navigate back to the first interface
                )
            ]
        )
    )
