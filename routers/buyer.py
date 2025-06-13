from fastapi import APIRouter
from sqlalchemy.orm import Session
from schemas.buyer import ItemBuyer
from fastapi import APIRouter, Depends, HTTPException, Header, Query
from routers.user_router import get_db
from models.buyer import Bayer
from models.inventry import Inventry
from models.user_auth import User, SessionToken
import base64
import json
from datetime import datetime, timedelta
from typing import List

router = APIRouter(
    prefix="/buyer",
    tags=["buyer"],  
)

@router.get("/")
async def get_companies():
    return [{"company": "ABC Corp"}, {"company": "XYZ Inc"}]



@router.post("/buy_item")
async def buy_item(item: ItemBuyer, session_id: str = Header(...), db: Session = Depends(get_db)):
    session = db.query(SessionToken).filter(SessionToken.token == session_id).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    db_item = Bayer(**item.dict())
    item_obj = db.query(Inventry).filter(Inventry.id == db_item.item_id, Inventry.is_deleted == False).first()
    if not item_obj:
        raise HTTPException(status_code=404, detail="Item not found")
    
    decoded_json = base64.b64decode(session.encrypt_session_data.encode()).decode()
    session_data = json.loads(decoded_json)

    db_item.buyer_id = session_data.get("user_id")
    db_item.seller_id = item_obj.user_id
    db_item.item_name = item_obj.item_name
    db_item.item_quantity = item_obj.item_total_quantity
    db_item.item_discription = item_obj.item_discription
    db_item.item_manu_date = item_obj.item_manu_date
    db_item.item_exp_date = item_obj.item_exp_date
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item



