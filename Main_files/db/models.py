from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    balance = Column(Float, nullable=False)
    email = Column(String, nullable=True)
    active = Column(Boolean, default=True)