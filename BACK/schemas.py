from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class SymptomRequest(BaseModel):
    symptoms: List[str]

class Doctor(BaseModel):
    id: int
    name: str
    specialization: str
    schedule: str

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    doctor_id: int
    user_id: int
    symptoms: str
    appointment_time: str

class Appointment(BaseModel):
    id: int
    doctor_id: int
    user_id: int
    symptoms: str
    appointment_time: str

    class Config:
        from_attributes = True
