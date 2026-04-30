from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.models.institute import Institute
from app.models.leads import Lead
from app.models.knowledge import Persona, KnowledgeBaseDocument
from app.models.script import Script
from app.models.conversations import Conversation, Message
from app.core import security

router = APIRouter()

@router.post("/seed", summary="Seed database with demo data (institute, user, leads, persona, script)")
def seed_data(db: Session = Depends(deps.get_db)):
    # 1. Create Institute
    demo_inst = db.query(Institute).filter(Institute.name == "Demo University").first()
    if not demo_inst:
        demo_inst = Institute(
            name="Demo University",
            email="admin@demouni.edu",
            onboarding_status=True
        )
        db.add(demo_inst)
        db.commit()
        db.refresh(demo_inst)
    
    # 2. Create Admin User
    demo_user = db.query(User).filter(User.email == "admin@demo.com").first()
    if not demo_user:
        demo_user = User(
            institute_id=demo_inst.id,
            full_name="Main Admin",
            email="admin@demo.com",
            password_hash=security.get_password_hash("admin123"),
            role="admin"
        )
        db.add(demo_user)
        db.commit()
    
    # 3. Add 5 Leads
    if db.query(Lead).filter(Lead.institute_id == demo_inst.id).count() == 0:
        leads = [
            Lead(institute_id=demo_inst.id, name="Rahul Sharma", phone="+91 9876543210", email="rahul@example.com", course="B.Tech", status="new"),
            Lead(institute_id=demo_inst.id, name="Priya Singh", phone="+91 9876543211", email="priya@example.com", course="MBA", status="contacting"),
            Lead(institute_id=demo_inst.id, name="Amit Patel", phone="+91 9876543212", email="amit@example.com", course="B.Sc", status="qualified"),
            Lead(institute_id=demo_inst.id, name="Sneha Reddy", phone="+91 9876543213", email="sneha@example.com", course="M.Tech", status="converted"),
            Lead(institute_id=demo_inst.id, name="Vikram Kumar", phone="+91 9876543214", email="vikram@example.com", course="BBA", status="lost")
        ]
        db.add_all(leads)
        db.commit()

    # 4. Add Persona
    if db.query(Persona).filter(Persona.institute_id == demo_inst.id).count() == 0:
        persona = Persona(
            institute_id=demo_inst.id,
            agent_name="Aditi",
            designation="Senior Admissions Counselor",
            tone_style="Professional and Warm",
            voice_gender="Female",
            voice_speed=1.0,
            persona_description="You are an expert counselor helping students choose the right engineering program."
        )
        db.add(persona)
        db.commit()

    # 5. Add Script
    if db.query(Script).filter(Script.institute_id == demo_inst.id).count() == 0:
        script = Script(
            institute_id=demo_inst.id,
            sections=[
                {"id": "intro", "title": "Introduction", "content": "Hello, I am Aditi from Demo University.", "isActive": True},
                {"id": "eligibility", "title": "Eligibility Check", "content": "May I know your 12th percentage?", "isActive": True}
            ]
        )
        db.add(script)
        db.commit()

    # 6. Add sample Conversation + Messages for lead #1
    lead = db.query(Lead).filter(Lead.name == "Rahul Sharma").first()
    if lead and db.query(Conversation).filter(Conversation.lead_id == lead.id).count() == 0:
        conv = Conversation(institute_id=demo_inst.id, lead_id=lead.id)
        db.add(conv)
        db.commit()
        db.refresh(conv)

        msg1 = Message(conversation_id=conv.id, speaker="ai", content="Hello Rahul, how can I help you today?")
        msg2 = Message(conversation_id=conv.id, speaker="user", content="I wanted to know more about B.Tech CSE.")
        db.add_all([msg1, msg2])
        db.commit()

    return {
        "message": "Demo data created",
        "data": {
            "user": {
                "email": "admin@demo.com",
                "password": "admin123"
            },
            "institute": "Demo University"
        }
    }
