import asyncio
from project.database import AsyncSessionLocal
from project.models import Job

async def seed_data():
    async with AsyncSessionLocal() as db:
        jobs = [
            Job(
                title="Python Backend Developer", 
                description="Build scalable APIs using FastAPI.", 
                qualifications="B.E/B.Tech, 2+ years Python experience",
                location="Remote", 
                salary=95000, 
                employer_id=1
            ),
            Job(
                title="Frontend Engineer (React)", 
                description="Develop modern user interfaces.", 
                qualifications="Proficiency in React and CSS",
                location="Chennai", 
                salary=75000, 
                employer_id=1
            ),
            Job(
                title="Data Scientist", 
                description="Analyze datasets using Python.", 
                qualifications="Experience with Pandas and Scikit-learn",
                location="Bangalore", 
                salary=120000, 
                employer_id=1
            ),
            Job(
                title="Full Stack Developer", 
                description="Knowledge of Python is a plus.", 
                qualifications="Experience with both SQL and NoSQL",
                location="Remote", 
                salary=105000, 
                employer_id=1
            ),
            Job(
                title="UI/UX Designer", 
                description="Design clean interfaces.", 
                qualifications="Strong portfolio in Figma/Adobe XD",
                location="Remote", 
                salary=70000, 
                employer_id=1
            )
        ]
        
        try:
            db.add_all(jobs)
            await db.commit()
            print("Successfully added 5 jobs to PostgreSQL!")
        except Exception as e:
            await db.rollback()
            print(f"Error seeding database: {e}")

if __name__ == "__main__":
    asyncio.run(seed_data())