from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///notify.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    balance = Column(Integer, default=5000)
    active = Column(Boolean, default=True)
    notifications = relationship("Notification", back_populates="employee")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    notifications = relationship("Notification", back_populates="user")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    read = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey("employees.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    employee = relationship("Employee", back_populates="notifications")
    user = relationship("User", back_populates="notifications")

Base.metadata.create_all(bind=engine)
if __name__ == "__main__":
    existing_employee = db.query(Employee).filter_by(email="aditya@example.com").first()
    if not existing_employee:
        employee = Employee(name="Aditya Raj", email="aditya@example.com")
        db.add(employee)
        db.commit()
        db.refresh(employee)
    else:
        employee = existing_employee

    existing_user = db.query(User).filter_by(username="admin").first()
    if not existing_user:
        user = User(username="admin")
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user = existing_user

    more_employees = [
        {"name": "Manvi Singh", "email": "manvi@example.com", "balance": "2000"},
        {"name": "Aryan Verma", "email": "aryan@example.com","balance": "800"},
        {"name": "Mandeep Kumar", "email": "mandeep@example.com0", "balance": "-1000"},
    ]

    for emp in more_employees:
        existing = db.query(Employee).filter_by(email=emp["email"]).first()
        if not existing:
            new_emp = Employee(name=emp["name"], email=emp["email"], balance=int(emp["balance"]))
            db.add(new_emp)
            db.commit()
            db.refresh(new_emp)
            print(f"Added employee: {new_emp.name}")
        else:
            print(f"Employee already exists: {existing.name}")

    more_users = ["manvi_user", "aryan_user", "mandeep_user"]

    for uname in more_users:
        existing = db.query(User).filter_by(username=uname).first()
        if not existing:
            new_user = User(username=uname)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print(f"Added user: {new_user.username}")
        else:
            print(f"User already exists: {existing.username}")

    existing_notification = db.query(Notification).filter_by(message="Welcome to Notify!").first()
    if not existing_notification:
        notification = Notification(
            message="Welcome to Notify!",
            employee_id=employee.id,
            user_id=user.id
        )
        db.add(notification)
        db.commit()

    employees = db.query(Employee).all()
    for e in employees:
        print(f"ID: {e.id}, Name: {e.name}, Email: {e.email}, Balance: {e.balance}, Active: {e.active}")

    duplicates = (
        db.query(Employee.email, func.count(Employee.id))
        .group_by(Employee.email)
        .having(func.count(Employee.id) > 1)
        .all()
    )

    for email, count in duplicates:
        dup_employees = db.query(Employee).filter_by(email=email).order_by(Employee.id).all()
        for emp in dup_employees[1:]:
            db.delete(emp)

    db.commit()

