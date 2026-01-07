import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def seed_database():
    url = "postgresql+asyncpg://postgres:bavaguru12@localhost:5432/job_listing_db"
    engine = create_async_engine(url)

    try:
        print("Connecting to job_listing_db...")
        async with engine.begin() as conn:
            # 1. Ensure at least one user exists to be the employer
            print("Checking for an employer/user...")
            user_check = await conn.execute(text("SELECT id FROM users LIMIT 1;"))
            user = user_check.fetchone()
            
            if not user:
                print("No user found. Creating a default employer...")
                await conn.execute(text("""
                    INSERT INTO users (email, hashed_password, full_name, role) 
                    VALUES ('admin@portal.com', 'dummyhash', 'Admin Employer', 'employer')
                """))
                user_check = await conn.execute(text("SELECT id FROM users LIMIT 1;"))
                user = user_check.fetchone()
            
            employer_id = user[0]
            print(f"Using Employer ID: {employer_id}")

            # 2. Clear existing jobs
            print("Cleaning up old job records...")
            await conn.execute(text("TRUNCATE TABLE jobs RESTART IDENTITY CASCADE;"))
            
            # 3. Insert fresh data with employer_id included
            print("Inserting fresh job data...")
            query = text("""
                INSERT INTO jobs (title, location, salary, description, qualifications, employer_id) 
                VALUES (:title, :location, :salary, :description, :qualifications, :employer_id)
            """)
            
            jobs = [
                {
                    "title": "Python Developer", "location": "Remote", "salary": 1200000, 
                    "description": "FastAPI backend development.", 
                    "qualifications": "Bachelor's in CS", "employer_id": employer_id
                },
                {
                    "title": "Frontend Engineer", "location": "Chennai", "salary": 800000, 
                    "description": "UI development with CSS.", 
                    "qualifications": "JS Proficiency", "employer_id": employer_id
                }
            ]
            
            for job in jobs:
                await conn.execute(query, job)
                
        print("Successfully seeded the database! ✅")
        
    except Exception as e:
        print(f"Error occurred during seeding: {e}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(seed_database())