from sqlalchemy import Column, Integer, String, Text
from .database import Base

class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer,index=True)
