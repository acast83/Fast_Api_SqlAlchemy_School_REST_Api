from pydantic import BaseModel
from enum import Enum
from typing import Optional


class Gender(str, Enum):
    male = "male"
    female = "female"


class StudentApiModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: Gender


class UpdateStudent(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[Gender] = None
