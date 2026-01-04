from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=schemas.JobPublic)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    # Note: In a real app, we'd get employer_id from the logged-in user.
    # For now, we are using a placeholder ID of 1 so you can test it.
    new_job = models.Job(**job.model_dump(), employer_id=1)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

@router.get("/", response_model=list[schemas.JobPublic])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(models.Job).all()