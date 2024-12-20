# from pydantic import BaseModel

# class EmployeeBase(BaseModel):
#     name: str
#     age: int

# class EmployeeWrite(EmployeeBase):
#     pass

# class EmployeeRead(EmployeeBase):
#     id: int

#     class Config:
#         orm_mode = True

# from pydantic import BaseModel, validator, root_validator, ValidationError
# from typing import Optional

# class EmployeeBase(BaseModel):
#     name: str
#     age: int

#     @validator('name')
#     def validate_name(cls, value):
#         if len(value) < 3:
#             raise ValueError('Name must be at least 3 characters long.')
#         return value
    
#     @validator('age')
#     def validate_age(cls, value):
#         if value <= 0:
#             raise ValueError('Age must be a positive integer.')
#         return value
    
#     class Config:
#         orm_mode = True

# class EmployeeWrite(EmployeeBase):
#     pass

# class EmployeeRead(EmployeeBase):
#     id: int

#     @root_validator(pre=True)
#     def validate_id(cls, values):
#         id_value = values.get('id')
#         if id_value is not None and id_value <= 0:
#             raise ValueError('ID must be a positive integer.')
#         return values
    
#     class Config:
#         orm_mode = True

# Example usage
# try:
#     employee = EmployeeWrite(name="Jo", age=25)
# except ValidationError as e:
#     print("Validation error:", e)

# try:
#     employee = EmployeeRead(id=-1, name="Alice", age=30)
# except ValidationError as e:
#     print("Validation error:", e)


from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, validator, ValidationError
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

# Models with validation
class EmployeeBase(BaseModel):
    name: str
    age: int

    @validator('name')
    def validate_name(cls, value):
        if len(value) < 3:
            raise ValueError('Name is too short (minimum 3 characters).')
        return value
    
    @validator('age')
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError('Age must be a positive number.')
        return value
    
    class Config:
        orm_mode = True

class EmployeeWrite(EmployeeBase):
    pass

class EmployeeRead(EmployeeBase):
    id: int

    class Config:
        orm_mode = True