from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from .db import Base

class Professor(Base):
    __tablename__ = "professors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    courses: Mapped[list["Course"]] = relationship(back_populates="professor", cascade="all, delete-orphan", single_parent=True,)

class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    professor_id: Mapped[int] = mapped_column(ForeignKey("professors.id", ondelete="RESTRICT"))
    professor: Mapped[Professor] = relationship(back_populates="courses")
