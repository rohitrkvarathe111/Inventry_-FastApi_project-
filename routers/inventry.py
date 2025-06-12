from fastapi import APIRouter
from sqlalchemy.orm import Session
from schemas.inventry import InventryCreate, ItemResponse, AllItemResponse
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from routers.user_router import get_db
from models.inventry import Inventry
from models.user_auth import User, SessionToken
import base64
import json
from datetime import datetime, timedelta
from typing import List

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


@router.get("/get_item", response_model=ItemResponse)
async def get_item(id: int , session_id: str = Header(...), db: Session = Depends(get_db)):
    session = db.query(SessionToken).filter(SessionToken.token == session_id).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    decoded_json = base64.b64decode(session.encrypt_session_data.encode()).decode()
    session_data = json.loads(decoded_json)
    user_id = session_data.get("user_id")
    # id = item_id.id
    db_item = db.query(Inventry).filter(Inventry.id == id, Inventry.user_id == user_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found for the given user.")

    return db_item



@router.delete("/delete_item", status_code=200)
async def get_item(id: int , session_id: str = Header(...), db: Session = Depends(get_db)):
    session = db.query(SessionToken).filter(SessionToken.token == session_id).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    decoded_json = base64.b64decode(session.encrypt_session_data.encode()).decode()
    session_data = json.loads(decoded_json)
    user_id = session_data.get("user_id")
    db_item = db.query(Inventry).filter(Inventry.id == id, Inventry.user_id == user_id, Inventry.is_deleted == False).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found for the given user.")

    db_item.is_deleted = True
    db.commit()

    return {"detail": "Item deleted successfully."}




@router.get("/get_all_item", response_model=List[AllItemResponse], status_code=200)
async def get_all_item(session_id: str = Header(...), db: Session = Depends(get_db),
                        page: int = Query(1, ge=1),
                        length: int = Query(10, gt=0)):
    session = db.query(SessionToken).filter(SessionToken.token == session_id).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    try:
        decoded_json = base64.b64decode(session.encrypt_session_data.encode()).decode()
        session_data = json.loads(decoded_json)
        user_id = session_data.get("user_id")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error decoding session data: {str(e)}")

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID not found in session data")

    try:
        offset = (page - 1) * length
        all_items = db.query(Inventry).filter(
            Inventry.user_id == user_id,
            Inventry.is_deleted == False
        ).offset(offset).limit(length).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

    return all_items