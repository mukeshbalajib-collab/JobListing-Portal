from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["job_seeker", "employer"]

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Role

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    role: Role
    is_active: bool
    created_at: datetime

# Job Schemas (For your module)
class JobCreate(BaseModel):
    title: str
    description: str
    qualifications: str
    location: str
    salary: Optional[int] = None

class JobPublic(JobCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    employer_id: int
    created_at: datetime
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"