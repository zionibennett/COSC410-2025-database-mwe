from __future__ import annotations

from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session, joinedload
from pathlib import Path


from .db import get_db
from . import models, schemas

app = FastAPI(title="DB MWE")


@app.get("/api/authors", response_model=list[schemas.AuthorOut])
def list_authors(db: Session = Depends(get_db)):
    return db.query(models.Author).order_by(models.Author.name).all()

@app.post("/api/authors", response_model=schemas.AuthorOut, status_code=201)
def create_author(payload: schemas.AuthorCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Author).filter_by(name=payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="Author already exists")
    a = models.Author(name=payload.name)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@app.get("/api/books", response_model=list[schemas.BookOut])
def list_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).options(joinedload(models.Book.author)).all()
    return [schemas.BookOut(id=b.id, title=b.title, author_id=b.author_id, author_name=b.author.name) for b in books]

@app.post("/api/books", response_model=schemas.BookOut, status_code=201)
def create_book(payload: schemas.BookCreate, db: Session = Depends(get_db)):
    author = db.get(models.Author, payload.author_id)
    if not author:
        raise HTTPException(status_code=400, detail="author_id not found")
    b = models.Book(title=payload.title, author_id=payload.author_id)
    db.add(b)
    db.commit()
    db.refresh(b)
    return schemas.BookOut(id=b.id, title=b.title, author_id=b.author_id, author_name=author.name)


FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

@app.get("/", response_class=FileResponse)
def index():
    return FileResponse(FRONTEND_DIR / "index.html")