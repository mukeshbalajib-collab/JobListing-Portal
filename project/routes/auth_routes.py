"""
project/routes/auth_routes.py
Comprehensive Auth, Rich Job Management, Success Messaging, and Prompt-Based Search.
"""

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# Standard relative imports to ensure package consistency
from ..auth import (
    clear_auth_cookie,
    create_access_token,
    get_current_user,
    get_current_user_optional,
    hash_password,
    require_role,
    set_auth_cookie,
    verify_password,
)
from ..database import get_db
from ..models import User, Job
from ..schemas import TokenResponse, UserCreate, UserLogin, UserPublic

templates = Jinja2Templates(directory="project/templates")
router = APIRouter()

# -------------------------
# AUTHENTICATION LOGIC
# -------------------------

@router.post("/auth/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
async def register_user(payload: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    """Registers a new user and hashes their password."""
    user = User(
        email=str(payload.email).lower(),
        hashed_password=hash_password(payload.password),
        role=payload.role,
        is_active=True,
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered.")
    await db.refresh(user)
    return user

@router.post("/auth/login", response_model=TokenResponse)
async def login_user(
    payload: UserLogin, 
    db: Annotated[AsyncSession, Depends(get_db)], 
    response: Response
):
    """Authenticates user and sets a secure JWT cookie."""
    result = await db.execute(select(User).where(User.email == str(payload.email).lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    
    token = create_access_token(subject=user.email, role=user.role)
    set_auth_cookie(response, token)
    return {"access_token": token, "token_type": "bearer"}

# -------------------------
# EMPLOYER: JOB MANAGEMENT
# -------------------------

@router.get("/post-job", response_class=HTMLResponse)
async def post_job_page(
    request: Request, 
    user: Annotated[User, Depends(require_role("employer"))]
):
    """Displays the professional job creation form."""
    return templates.TemplateResponse("post_job.html", {"request": request, "email": user.email})

@router.post("/jobs/submit")
async def handle_post_job(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    title: str = Form(...),
    description: str = Form(...),
    location: str = Form(...),
    qualifications: str = Form(...),
    salary: Optional[int] = Form(None)
):
    """Saves job listing and redirects to dashboard with a success trigger."""
    new_job = Job(
        title=title,
        description=description,
        location=location,
        qualifications=qualifications,
        salary=salary,
        employer_id=user.id
    )
    db.add(new_job)
    await db.commit()
    
    # Redirect with query param to trigger 'Success' toast in UI
    return RedirectResponse(
        url="/dashboard/employer?msg=success", 
        status_code=status.HTTP_303_SEE_OTHER
    )

# -------------------------
# JOB SEEKER: BROWSE & SEARCH
# -------------------------

@router.get("/jobs/browse", response_class=HTMLResponse)
async def browse_jobs_page(
    request: Request, 
    user: Annotated[User, Depends(require_role("job_seeker"))]
):
    """Serves the primary Job Discovery/Search page."""
    return templates.TemplateResponse("browse_jobs.html", {
        "request": request,
        "email": user.email
    })

@router.get("/jobs/search/api")
async def search_jobs_api(
    db: Annotated[AsyncSession, Depends(get_db)],
    keyword: Optional[str] = Query(None),
    location: Optional[str] = Query(None)
):
    """High-feature API for prompt-based filtering (AJAX)."""
    stmt = select(Job)
    if keyword:
        # Prompt-based search looks in title AND description
        stmt = stmt.where(
            or_(
                Job.title.ilike(f"%{keyword}%"),
                Job.description.ilike(f"%{keyword}%")
            )
        )
    if location:
        stmt = stmt.where(Job.location.ilike(f"%{location}%"))

    result = await db.execute(stmt)
    return result.scalars().all()

# -------------------------
# NAVIGATION & DASHBOARDS
# -------------------------

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_redirect(
    request: Request,
    user: Annotated[User | None, Depends(get_current_user_optional)],
):
    """Smart routing: prevents 404s by sending users to their specific UI."""
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    if user.role == "job_seeker":
        return RedirectResponse(url="/dashboard/jobseeker", status_code=status.HTTP_302_FOUND)
    elif user.role == "employer":
        return RedirectResponse(url="/dashboard/employer", status_code=status.HTTP_302_FOUND)
    
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.get("/dashboard/employer", response_class=HTMLResponse)
async def employer_dashboard(
    request: Request, 
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(require_role("employer"))]
):
    """Displays employer-specific job listings."""
    result = await db.execute(select(Job).where(Job.employer_id == user.id))
    jobs = result.scalars().all()
    return templates.TemplateResponse(
        "employer_dashboard.html", 
        {"request": request, "email": user.email, "jobs": jobs}
    )

@router.get("/dashboard/jobseeker", response_class=HTMLResponse)
async def jobseeker_dashboard(
    request: Request, 
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(require_role("job_seeker"))]
):
    """Detailed Seeker Dashboard with dynamic KPI cards."""
    # Placeholder stats to match your HTML KPI card requirements
    stats = {
        "total": 0,
        "pending": 0,
        "accepted": 0,
        "rejected": 0
    }
    
    return templates.TemplateResponse(
        "jobseeker_dashboard.html", 
        {
            "request": request, 
            "email": user.email, 
            "role": user.role,
            "stats": stats,
            "applications": [] # Currently empty to show 'Empty State' UI
        }
    )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Serves the login page."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/logout")
async def logout():
    """Clears session and redirects to login."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    clear_auth_cookie(response)
    return response
# Add this route to fix the 404 error for /register
@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Serves the registration page to new users."""
    return templates.TemplateResponse("register.html", {"request": request})
