from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from src.Models.base import Base

class Subject(Base, table=True):
    __tablename__ = "subject"

    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(index=True)           # subject name
    matiere: str                           # course/module name
    coefficient: int                       # positive integer
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    owner_id: int = Field(foreign_key="user.id")