from fastapi import APIRouter
from sqlalchemy.orm import Session
from schemas.inventry import InventryCreate
from fastapi import APIRouter, Depends, HTTPException, Header
from routers.user_router import get_db
from models.inventry import Inventry
from models.user_auth import User, SessionToken
import base64
import json
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/inventry",
    tags=["Inventry"],  # Unique tag name
)

@router.get("/")
async def get_companies():
    return [{"company": "ABC Corp"}, {"company": "XYZ Inc"}]



@router.post("/create_item")
async def create_item(item: InventryCreate, session_id: str = Header(...), db: Session = Depends(get_db)):
    db_item = Inventry(**item.dict())
    session = db.query(SessionToken).filter(SessionToken.token == session_id).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    decoded_json = base64.b64decode(session.encrypt_session_data.encode()).decode()
    session_data = json.loads(decoded_json)

    db_item.user_id = session_data.get("user_id")
    print(db_item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item