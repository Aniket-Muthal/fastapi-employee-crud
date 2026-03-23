from app import crud
from typing import List
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal, Base
from fastapi import FastAPI, status, HTTPException, Depends
from app.schemas import EmployeeCreate, EmployeeUpdate, EmployeeOut


Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employees", response_model=EmployeeOut)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db_session=db, employee=employee)


@app.get("/employees", response_model=List[EmployeeOut])
def get_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db_session=db)


@app.get("/employees/{emp_id}", response_model=EmployeeOut)
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    db_employee = crud.get_employee(db_session=db, emp_id=emp_id)

    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {emp_id} not found."
        )
    return db_employee


@app.put("/update_employee/{emp_id}", response_model=EmployeeOut)
def update_employee(emp_id: int, employee: EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud.update_employee(db_session=db, emp_id=emp_id, employee=employee)

    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {emp_id} not found."
        )
    return db_employee


@app.delete("/delete_employee/{emp_id}", response_model=dict)
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    db_employee = crud.delete_employee(db_session=db, emp_id=emp_id)
    if db_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id: {emp_id} not found."
        )
    return {"message": f"Employee with id: {emp_id} deleted successfully."}