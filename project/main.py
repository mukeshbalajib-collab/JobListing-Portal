from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import Optional

load_dotenv()

try: 
    from database import engine, get_db
    from models import Base, Job
    from routes.auth_routes import router as auth_router
    from profile_service.routes.profile_routes import router as profile_router
    from profile_service.database import engine as profile_engine
    from profile_service.models import Base as ProfileBase
except ImportError:
    from project.database import engine, get_db
    from project.models import Base, Job
    from project.routes.auth_routes import router as auth_router
    from project.profile_service.routes.profile_routes import router as profile_router
    from project.profile_service.database import engine as profile_engine
    from project.profile_service.models import Base as ProfileBase

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with profile_engine.begin() as conn:
        await conn.run_sync(ProfileBase.metadata.create_all)
    yield

app = FastAPI(title="Job Listing Portal", lifespan=lifespan)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

PROFILE_SERVICE_DIR = os.path.join(BASE_DIR, "profile_service")
PROFILE_UPLOADS_DIR = os.path.join(PROFILE_SERVICE_DIR, "uploads")
if os.path.isdir(PROFILE_UPLOADS_DIR):
    app.mount("/uploads", StaticFiles(directory=PROFILE_UPLOADS_DIR), name="uploads")

app.include_router(auth_router)
app.include_router(profile_router)

@app.get("/jobs/search", tags=["Job Search"])
async def search_jobs(
    keyword: Optional[str] = Query(None),
    location: Optional[str] = Query(None),
    min_salary: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Job)
    if keyword:
        stmt = stmt.where(
            or_(
                Job.title.ilike(f"%{keyword}%"),
                Job.description.ilike(f"%{keyword}%")
            )
        )
    if location:
        stmt = stmt.where(Job.location.ilike(f"%{location}%"))
    if min_salary:
        stmt = stmt.where(Job.salary >= min_salary)

    result = await db.execute(stmt)
    return result.scalars().all()

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard", status_code=302)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)