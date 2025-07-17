from db.database import SessionLocal
from db.models import Employee

db = SessionLocal()
employees = db.query(Employee).all()

if not employees:
    print("🚫 No employees found in the database.")
else:
    print("✅ Current Employees in the Database:")
    for emp in employees:
        print(f"ID: {emp.id}, Name: {emp.name}, Balance: {emp.balance}, Email: {emp.email}, Active: {emp.active}")

db.close()
