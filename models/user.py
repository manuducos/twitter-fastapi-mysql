# Python
from typing import Optional
from datetime import date

# Pydantic
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr = Field(...)
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserOut(UserBase):
    id: Optional[int]

class UserRegister(UserBase):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64
    )