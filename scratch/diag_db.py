from app.db.session import SessionLocal
from app.models.institute import Institute
from app.models.user import User
from app.core import security

db = SessionLocal()
try:
    print("Checking database connection...")
    inst = db.query(Institute).first()
    print(f"Institute: {inst.name if inst else 'None'}")
    
    user = db.query(User).first()
    print(f"User: {user.full_name if user else 'None'}")
finally:
    db.close()
