from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from pathlib import Path


from .db import get_db
from . import models, schemas

app = FastAPI(title="DB MWE")


@app.get("/api/professors", response_model=list[schemas.ProfessorOut])
def list_professors(db: Session = Depends(get_db)):
    return db.query(models.Professor).order_by(models.Professor.name).all()

@app.post("/api/professors", response_model=schemas.ProfessorOut, status_code=201)
def create_professor(payload: schemas.ProfessorCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Professor).filter_by(name=payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Professor already exists")
    a = models.Professor(name=payload.name)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@app.get("/api/courses", response_model=list[schemas.CourseOut])
def list_courses(db: Session = Depends(get_db)):
    courses = db.query(models.Course).options(joinedload(models.Course.professor)).all()
    return [schemas.CourseOut(id=b.id, title=b.title, professor_id=b.professor_id, professor_name=b.professor.name) for b in courses]

@app.post("/api/courses", response_model=schemas.CourseOut, status_code=201)
def create_course(payload: schemas.CourseCreate, db: Session = Depends(get_db)):
    professor = db.get(models.Professor, payload.professor_id)
    if not professor:
        raise HTTPException(status_code=400, detail="professor_id not found")
    b = models.Course(title=payload.title, professor_id=payload.professor_id)
    db.add(b)
    db.commit()
    db.refresh(b)
    return schemas.CourseOut(id=b.id, title=b.title, professor_id=b.professor_id, professor_name=professor.name)


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")