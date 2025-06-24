from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    specialization = Column(String)
    schedule = Column(String)  # CSV слотов
    symptoms = relationship("Symptom", secondary="doctor_symptoms")

class Symptom(Base):
    __tablename__ = "symptoms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

class DoctorSymptom(Base):
    __tablename__ = "doctor_symptoms"
    doctor_id = Column(Integer, ForeignKey("doctors.id"), primary_key=True)
    symptom_id = Column(Integer, ForeignKey("symptoms.id"), primary_key=True)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    symptoms = Column(String)
    appointment_time = Column(String)
    doctor = relationship("Doctor")
    user = relationship("User")
