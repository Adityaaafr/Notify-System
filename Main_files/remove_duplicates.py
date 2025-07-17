from db.database import SessionLocal
from db.models import Employee
from sqlalchemy import func

db = SessionLocal()

# Step 1: Get duplicate names with more than 1 entry
duplicate_names = (
    db.query(Employee.name)
    .group_by(Employee.name)
    .having(func.count(Employee.name) > 1)
    .all()
)

for name_tuple in duplicate_names:
    name = name_tuple[0]

    # Step 2: Get all employees with that name
    employees = db.query(Employee).filter(Employee.name == name).all()

    # Step 3: Keep the first, delete the rest
    for emp in employees[1:]:
        print(f"Deleting duplicate: {emp.name} with ID: {emp.id}")
        db.delete(emp)

db.commit()
db.close()
