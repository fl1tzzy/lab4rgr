from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

import models, crud, schemas, auth
from database import SessionLocal, engine

# Создаём таблицы
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    if db.query(models.Doctor).count() == 0:
        # Симптомы
        names = ["головная боль","кашель","лихорадка","геморрой",
                 "боль в спине","тошнота","насморк","боль в животе"]
        db.add_all([models.Symptom(name=n) for n in names])
        db.commit()

        # Врачи
        doctors = [
            ("Иванов Иван","Терапевт","9:00,10:00,11:00"),
            ("Петров Пётр","Хирург","10:00,12:00,14:00"),
            ("Сидоров Сергей","Кардиолог","9:30,11:30,13:30"),
            ("Кузнецова Анна","Педиатр","10:00,11:00,12:00,15:00"),
            ("Морозов Дмитрий","Невролог","9:00,11:00,13:00,16:00"),
        ]
        for name, spec, sched in doctors:
            db.add(models.Doctor(name=name, specialization=spec, schedule=sched))
        db.commit()

        # Связи
        all_symps = {s.name: s.id for s in db.query(models.Symptom).all()}
        all_docs  = {d.name: d.id for d in db.query(models.Doctor).all()}
        mapping = {
            "Иванов Иван":["головная боль","кашель","насморк"],
            "Петров Пётр":["боль в животе","геморрой","тошнота"],
            "Сидоров Сергей":["боль в спине","головная боль"],
            "Кузнецова Анна":["кашель","лихорадка","насморк"],
            "Морозов Дмитрий":["головная боль","боль в спине","тошнота"],
        }
        rels = []
        for doc_name, sym_list in mapping.items():
            doc_id = all_docs[doc_name]
            for sym in sym_list:
                rels.append(models.DoctorSymptom(doctor_id=doc_id, symptom_id=all_symps[sym]))
        db.add_all(rels)
        db.commit()
    db.close()

@app.post("/register/", response_model=schemas.UserOut, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print(user)
    return crud.create_user(db, user)

@app.post("/login/")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.authenticate_user(db, user)
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверные учётные данные")
    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post(
    "/doctors-by-symptoms/",
    response_model=List[schemas.Doctor],
    dependencies=[Depends(auth.get_current_user)]
)
def doctors_by_symptoms(req: schemas.SymptomRequest, db: Session = Depends(get_db)):
    return crud.get_doctors_by_symptoms(db, req.symptoms)

@app.post(
    "/appointments/",
    response_model=schemas.Appointment,
    dependencies=[Depends(auth.get_current_user)]
)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appointment)
