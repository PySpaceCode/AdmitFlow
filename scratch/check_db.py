import sys
import os
sys.path.append(os.getcwd())

from app.db.session import engine, Base
import app.models

def check_tables():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("Tables in database:", tables)
    
    if "users" in tables:
        print("[OK] 'users' table exists.")
    else:
        print("[MISSING] 'users' table MISSING.")
        print("Attempting to create all tables...")
        Base.metadata.create_all(bind=engine)
        tables_after = inspect(engine).get_table_names()
        print("Tables after create_all:", tables_after)
        if "users" in tables_after:
            print("[OK] 'users' table created successfully.")
        else:
            print("[ERROR] FAILED to create 'users' table.")


if __name__ == "__main__":
    check_tables()
