from sqlalchemy.orm import Session
from app.models import Employee
from app.schemas import *


def get_employees(db_session: Session):
    return (
        db_session
        .query(Employee)
        .all()
    )


def get_employee(db_session: Session, emp_id: int):
    return(
        db_session
        .query(Employee)
        .filter(Employee.id == emp_id)
        .first()
    )


def create_employee(db_session: Session, employee: EmployeeCreate):
    db_employee = Employee(
        name=employee.name,
        email=employee.email
    )
    db_session.add(db_employee)
    db_session.commit()
    db_session.refresh(db_employee)

    return db_employee


def update_employee(db_session: Session, emp_id: int, employee: EmployeeUpdate):
    db_employee = (
        db_session
        .query(Employee)
        .filter(Employee.id == emp_id)
        .first()
    )

    if db_employee:
        db_employee.name = employee.name
        db_employee.email = employee.email
        db_session.commit()
        db_session.refresh(db_employee)

    return db_employee


def delete_employee(db_session: Session, emp_id: int):
    db_employee = (
        db_session
        .query(Employee)
        .filter(Employee.id == emp_id)
        .first()
    )

    if db_employee:
        db_session.delete(db_employee)
        db_session.commit()
    
    return db_employee