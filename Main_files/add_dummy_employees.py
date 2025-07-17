from db.database import SessionLocal
from db.models import Employee

# Create a database session
db = SessionLocal()

# Dummy employee data
dummy_employees = [
    Employee(name="Charlie", balance=7000.0, email="charlie@example.com", active=False),
    Employee(name="Veronica", balance=1200.0, email="Veronica@example.com", active=True),
    Employee(name="Bhagat", balance=900.0, email="Bhagat@example.com", active=True),
    Employee(name="Sheesh", balance=-1300.0, email="Sheesh@example.com", active=True),
    Employee(name="Manya", balance=650.0, email="Manya@example.com", active=True),
    Employee(name="Ben", balance=-1000.0, email="Ben@example.com", active=True),
]

# Add the dummy employees to the session
db.add_all(dummy_employees)

# Commit the changes to the database
db.commit()

# Close the session
db.close()

print("✅ Dummy employees added successfully.")
