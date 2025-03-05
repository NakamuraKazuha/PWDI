from sqlalchemy import create_engine, text

# Connect to your database
engine = create_engine("sqlite:///users.db")

# Execute ALTER TABLE commands
with engine.connect() as connection:
    connection.execute(text("ALTER TABLE profiles ADD COLUMN address TEXT;"))
    connection.execute(text("ALTER TABLE profiles ADD COLUMN contact_number TEXT;"))

print("Columns added successfully!")
