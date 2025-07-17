from sqlalchemy.orm import Session
from .models import Employee

def get_all_employees(db: Session):
    return db.query(Employee).all()

def update_employee_balance(db: Session, emp_id: int, new_balance: float):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if emp:
        emp.balance = new_balance
        db.commit()
        db.refresh(emp)
        return emp
    return None
