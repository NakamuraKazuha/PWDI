from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, DateTime, Date #define the data types
from sqlalchemy.ext.declarative import declarative_base #python class
from sqlalchemy.orm import sessionmaker #database transaction 
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash #for the extra security idk if this will work


# Database setup
db_file = "users.db"
engine = create_engine(f"sqlite:///{db_file}", echo=True) #connects to the database, echo just prints the queries sa terminal(debug purposes)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() #the base class

# Define the models
class Users(Base):
    __tablename__ = "users" #this is the name for the table (mr.obvious)
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    consent = Column(Boolean, nullable=False, default=False)
    legal = Column(Boolean, nullable=False, default=False)

class AuthorizedViewers(Base):
    __tablename__ = "authorized_viewers"
    owner_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    viewer_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)

class AccessibleUser(Base):
    __tablename__ = "accessible_users"
    user_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))  # the user receiving the notification
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=func.now())  #naa time



class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, autoincrement=True) 
    username = Column(String, unique=True, nullable=False)  
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    medical_condition = Column(String, nullable=True) 
    mobility_issues = Column(String, nullable=True)  
    address = Column(String, nullable=True) 
    contact_number = Column(String, nullable=True) 

class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    primary_diagnosis = Column(String, nullable=False)
    other_conditions = Column(String, nullable=True)
    medication_name = Column(String, nullable=True)
    medication_dosage = Column(String, nullable=True)
    medication_frequency = Column(String, nullable=True)
    allergies = Column(String, nullable=True)
    surgery_year = Column(String, nullable=True)
    surgery_name = Column(String, nullable=True)
    hospital_name = Column(String, nullable=True)

Base.metadata.create_all(engine) #this creates the table

#creates the session, used fro queries basically (add, update, or remove records)
Session = sessionmaker(bind=engine)
session = Session()


def register_user(name, email, password):
    session = Session()
    
    # Check if email already exists
    if session.query(Users).filter_by(email=email).first():
        return False, "Email already registered."
    
    # Hash password before storing
    password_hash = generate_password_hash(password)
    new_user = Users(name=name, email=email, password_hash=password_hash)
    
    session.add(new_user)
    session.commit()
    return True, "Registration successful."

def verify_user(name, password):
    session = Session()
    user = session.query(Users).filter_by(name=name).first()
    if user and check_password_hash(user.password_hash, password):
        return True, "Login successful."
    return False, "Invalid username or password."





#a query -> fetches the name and returns a list.
def fetch_users():
    return [(user.user_id, user.name) for user in session.query(Users).all()]

def fetch_auth_viewers(user_id):
    if isinstance(user_id, list):  
        user_id = user_id[0]  # Extract first value if list

    return [av.viewer_id for av in session.query(AuthorizedViewers).filter_by(owner_id=user_id).all()]


def fetch_acc_users(viewer_id):
    owners = session.query(AuthorizedViewers.owner_id).filter_by(viewer_id=viewer_id).all()
    return [(user.user_id, user.name) for user in session.query(Users).filter(Users.user_id.in_([o[0] for o in owners])).all()]

def fetch_notifications(user_id):
    notifications = session.query(Notification).filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()
    return [(n.id, n.message) for n in notifications]

#Section: Notification
def get_notifications(user_id):
    return session.query(Notification).filter_by(user_id=user_id).order_by(Notification.timestamp.desc()).all()

def send_notification(user_id, message):
    new_notification = Notification(user_id=user_id, message=message)
    session.add(new_notification)
    session.commit()
    print(f"Notification sent to User {user_id}: {message}")

#Section: add
def add_user(user_id, name):
    if not session.query(Users).filter_by(user_id=user_id).first(): #Check Users table
        session.add(Users(user_id=user_id, name=name)) #add to Users table
        session.commit()
        print(f"User '{name}' with ID {user_id} added to Users.")
    else:
        print(f"User ID {user_id} already exists in Users.")

def add_authorized_viewer(owner_id, viewer_id):
    if session.query(Users).filter_by(user_id=viewer_id).first():
        if not session.query(AuthorizedViewers).filter_by(owner_id=owner_id, viewer_id=viewer_id).first():
            session.add(AuthorizedViewers(owner_id=owner_id, viewer_id=viewer_id))
            session.commit()
            print(f"User ID {viewer_id} is now authorized to view {owner_id}.")
            owner = session.query(Users).filter_by(user_id=owner_id).first()
            if owner:
                send_notification(viewer_id, f"You have been added as an authorized viewer by {owner.name}.")

        else:
            print(f"User ID {viewer_id} is already authorized.")
    else:
        print(f"User ID {viewer_id} does not exist.")

def add_accessible_user(viewer_id, owner_id):
    if session.query(AuthorizedViewers).filter_by(owner_id=owner_id, viewer_id=viewer_id).first():
        owner = session.query(Users).filter_by(user_id=owner_id).first()
        if owner and not session.query(AccessibleUser).filter_by(user_id=owner_id).first():
            session.add(AccessibleUser(user_id=owner.user_id, name=owner.name))
            session.commit()
            print(f"User ID {owner_id} ('{owner.name}') is now accessible to {viewer_id}.")
        else:
            print(f"User ID {owner_id} is already accessible.")
    else:
        print(f"User ID {owner_id} has not authorized {viewer_id} as a viewer.")


#section: remove
def remove_acc_user(viewer_id, owner_id):
    session.query(AuthorizedViewers).filter_by(owner_id=owner_id, viewer_id=viewer_id).delete()
    remaining_viewers = session.query(AuthorizedViewers).filter_by(owner_id=owner_id).first()
    if not remaining_viewers:
        session.query(AccessibleUser).filter_by(user_id=owner_id).delete()
    
    session.commit()


def remove_auth_viewer(owner_id, viewer_id):
    user = session.query(AuthorizedViewers).filter_by(owner_id=owner_id, viewer_id=viewer_id).first()
    if user:
        session.delete(user) #we delete the user only from the it being an accessible user
        session.commit()
        
def print_table_data():
    models = [Users, AuthorizedViewers, AccessibleUser, Notification, Profile, MedicalHistory]
    for model in models:
        print(f"\nTable: {model.__tablename__}")
        print("-" * (len(model.__tablename__) + 8))

        # Fetch all records from the table
        records = session.query(model).all()

        if not records:
            print("No data available.")
            continue
        
        # Print column headers
        column_names = model.__table__.columns.keys()
        print(" | ".join(column_names))
        print("-" * 50)

        # Print each row
        for record in records:
            values = [str(getattr(record, col)) for col in column_names]
            print(" | ".join(values))

    # to test if okay ra ang consent and legal
    print("\nTable: Users")
    print("-" * 20)
    users = session.query(Users).all()
    if users:
        print("User ID | Name | Email | Consent | Legal")
        print("-" * 50)
        for user in users:
            print(f"{user.user_id} | {user.name} | {user.email} | {user.consent} | {user.legal}")
    else:
        print("No users found.")

# This is just for the terminal, because it would mess up my front end. I made the data here kay wala pa ka melo
def main():
    print("\nUsers:", fetch_users())

    #asks for the ID (mura login in sa sya for now)
    viewer_id = input("Enter your 6-digit User ID to check accessible users: ").strip()
    if not (viewer_id.isdigit() and len(viewer_id) == 6):
        print("Invalid ID. Must be a 6-digit number.")
        return  # Exit if the input is invalid

    viewer_id = int(viewer_id)  # Convert to integer for database queries
    notifications = fetch_notifications(viewer_id)

    while True:
        print("\nAccessible Users:", fetch_acc_users(viewer_id))
        print("Authorized Viewers:", fetch_auth_viewers(viewer_id))
        
        print("\nOptions:")
        print("1. Add User")
        print("2. Add Authorized Viewer")
        print("3. Remove Access")
        print("4. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            user_id = input("Enter 6-digit User ID: ").strip()
            name = input("Enter username to add: ").strip()
            if user_id.isdigit() and len(user_id) == 6 and name:
                add_user(int(user_id), name)
            else:
                print("Invalid ID. Must be a 6-digit number.")

        elif choice == "2":
            viewer_to_add = input("Enter Viewer ID to authorize: ").strip()
            if viewer_to_add.isdigit() and len(viewer_to_add) == 6:
                add_authorized_viewer(viewer_id, int(viewer_to_add)) 
            else:
                print("Invalid Viewer ID. Must be a 6-digit number.")

        elif choice == "3":
            owner_id = input("Enter User ID to remove accessible: ").strip()
            if owner_id.isdigit() and len(owner_id) == 6:
                remove_acc_user(viewer_id, int(owner_id))  
            else:
                print("Invalid User ID. Must be a 6-digit number.")

        elif choice == "4":
            print("Bye Bye")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    print_table_data()
    main()
