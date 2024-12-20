import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Employee
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

# Create a testing database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create an engine and session for the testing database
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency to use the test database session
@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

# Use TestClient to send requests to FastAPI
@pytest.fixture(scope="module")
def client():
    client = TestClient(app)
    return client

# Test POST /create endpoint
def test_create_employee(client, db):
    employee_data = {"name": "John Doe", "age": 30}
    
    response = client.post("/create", json=employee_data)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Employee Created Successfully", "status": 200}

# Test GET /read endpoint
def test_read_employees(client, db):
    employee_data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 35}]
    
    # Add employees to the database
    for emp in employee_data:
        db.add(Employee(**emp))
    db.commit()

    response = client.get("/read")
    
    assert response.status_code == 200

# Test GET /detail endpoint
def test_detail_employee(client, db):
    employee = Employee(name="Charlie", age=40)
    db.add(employee)
    db.commit()
    
    response = client.get(f"/detail?id={employee.id}")
    
    assert response.status_code == 200

def test_detail_employee_not_found(client):
    response = client.get("/detail?id=9999")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee Not Found"}

# Test PATCH /update endpoint
def test_update_employee(client, db):
    employee = Employee(name="David", age=45)
    db.add(employee)
    db.commit()
    
    updated_data = {"name": "David Updated", "age": 46}
    response = client.patch(f"/update?id={employee.id}", json=updated_data)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Employee Updated Successfully", "status": 200}
    

def test_update_employee_not_found(client):
    updated_data = {"name": "Not Found", "age": 50}
    response = client.patch("/update?id=9999", json=updated_data)
    
    assert response.status_code == 404
    assert response.json() == {"detail": "Employee Not Found"}

# Test DELETE /delete-user endpoint
def test_delete_employee(client, db):
    employee = Employee(name="Jhone Doe", age=30)
    db.add(employee)
    db.commit()
    
    response = client.delete(f"/delete-user?id={employee.id}")
    
    assert response.status_code == 404

