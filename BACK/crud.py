from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
import bcrypt, models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    hashed = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user.hashed_password):
        return False
    return db_user

def get_doctors_by_symptoms(db: Session, symptoms: list):
    doctors = db.query(models.Doctor).options(joinedload(models.Doctor.symptoms)).all()
    scored = []
    for doc in doctors:
        doc_syms = {s.name.lower() for s in doc.symptoms}
        cnt = sum(1 for s in symptoms if s.lower() in doc_syms)
        if cnt > 0: scored.append((doc, cnt))
    if not scored: return []
    max_cnt = max(cnt for _, cnt in scored)
    return [doc for doc, cnt in scored if cnt == max_cnt]

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_app = models.Appointment(**appointment.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app
