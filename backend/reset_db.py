import sys
import os

# Add the current directory to sys.path
sys.path.append(os.getcwd())

from sqlalchemy import text
from app.db.session import engine

def reset_database():
    print("Starting Database Reset...")
    try:
        with engine.connect() as conn:
            # 1. Terminate other connections to avoid locking
            print("Closing other active connections...")
            conn.execute(text("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = current_database()
                  AND pid <> pg_backend_pid();
            """))
            conn.commit()

            # 2. DROP EVERYTHING
            print("Dropping all tables and constraints (CASCADE)...")
            # Dropping the schema is the most reliable way to clear mismatched types
            conn.execute(text("DROP SCHEMA public CASCADE;"))
            conn.execute(text("CREATE SCHEMA public;"))
            
            # 3. Restore necessary permissions
            print("Restoring schema permissions...")
            conn.execute(text("GRANT ALL ON SCHEMA public TO postgres;"))
            conn.execute(text("GRANT ALL ON SCHEMA public TO public;"))
            
            conn.commit()
            print("OK. Database is now CLEAN and ready for the new schema.")
            print("\nNext Steps:")
            print("1. Run the backend: uvicorn app.main:app --reload")
            print("2. Run the seed: Invoke-WebRequest -Method Post -Uri http://localhost:8000/api/dev/seed")
            
    except Exception as e:
        print(f"❌ CRITICAL ERROR resetting database: {e}")
        print("\nPossible solutions:")
        print("- Ensure no pgAdmin or SQL terminal is currently looking at the 'public' tables.")
        print("- Ensure the backend process is STOPPED before running this script.")

if __name__ == "__main__":
    reset_database()
