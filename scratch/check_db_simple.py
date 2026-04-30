import sys
import os
sys.path.append(os.getcwd())

from app.db.session import engine, Base
import app.models

def check_tables():
    from sqlalchemy import inspect
    inspector = inspect(engine)
    try:
        tables = inspector.get_table_names()
        print("Initial tables:", tables)
    except Exception as e:
        print("Error getting initial tables:", e)

    print("Attempting create_all...")
    try:
        Base.metadata.create_all(bind=engine)
        print("create_all completed.")
    except Exception as e:
        print("create_all failed with error:")
        print(e)
        
    try:
        tables = inspect(engine).get_table_names()
        print("Final tables:", tables)
    except Exception as e:
        print("Error getting final tables:", e)

if __name__ == "__main__":
    check_tables()
