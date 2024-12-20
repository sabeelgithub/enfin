from fastapi import FastAPI, Depends, HTTPException,status,Request
from sqlalchemy.orm import Session
from typing import List,Annotated
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .database import engine,get_db,Base
from .schemas import EmployeeWrite,EmployeeRead
from .models import Employee

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Dependency
# get_db = database.get_db

db_dependency = Annotated[Session,Depends(get_db)]

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Collect error messages
    error_messages = [str(e["msg"]) for e in exc.errors()]
    return JSONResponse(
        status_code=400,
        content={"detail": error_messages}
    )

@app.post("/create")
async def create_employee(employee:EmployeeWrite,db:db_dependency):
    """
    This endpoint is responsible for creating employees
    """
    db_employee = Employee(name=employee.name,age=employee.age)
    db.add(db_employee)
    db.commit()
    return {"message":"Employee Created Successfully","status":status.HTTP_200_OK}

@app.get("/read",response_model=List[EmployeeRead])
async def read_employees(db:db_dependency):
    """
    This endpoint is responsible for reading all employees
    """
    employees = db.query(Employee).all()
    return employees

@app.get("/detail",response_model=EmployeeRead)
async def detail_employee(db:db_dependency,id:int):
    """
    This endpoint is responsible for reading single employee by id
    """
    employee = db.query(Employee).get(id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee Not Found")
    return employee

@app.patch("/update")
async def update_employee(db:db_dependency,id:int,request_data:EmployeeWrite):
    """
    This endpoint is responsible for updating employees
    """
    employee = db.query(Employee).get(id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee Not Found")
    
    employee.name = request_data.name
    employee.age = request_data.age
    db.commit()
    return {"message":"Employee Updated Successfully","status":status.HTTP_200_OK}

@app.delete("/delete-user")
async def delete_employee(db:db_dependency,id:int):
    """
    This endpoint is responsible for deleting employee 
    """
    employee = db.query(Employee).get(id)
    if employee is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Employee Not Found")
    
    db.delete(employee)
    db.commit()
    return {"message":"Employee Deleted Successfully","status":status.HTTP_200_OK}