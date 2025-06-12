from fastapi import APIRouter
from schemas.user_auth import UserCreate, UserLogin, UserLogout
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_auth import User, SessionToken
from fastapi import APIRouter, Depends, HTTPException, Header
from passlib.context import CryptContext
import secrets
import base64
import json
from datetime import datetime, timedelta


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/base")
def base_root():
    return {"message": "hello sir"}


def get_password_hash(password):
    return pwd_context.hash(password)


@router.post("/create_user", status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists.")

    hashed_password = get_password_hash(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        middle_name=user.middle_name,
        last_name=user.last_name,
        mobile_number=user.mobile_number,
        is_admin=user.is_admin,
        is_active=user.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}


@router.post("/login", status_code=200)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user or not pwd_context.verify(user_credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    login_data = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "mobile_number": user.mobile_number,
    }
    session_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(days=1)
    
    login_data_json = json.dumps(login_data).encode()
    encoded_data = base64.b64encode(login_data_json).decode()
    login_data["session_id"] = session_token
    session = SessionToken(
        user_id=user.id,
        token=session_token,
        expires_at=expires_at,
        encrypt_session_data=encoded_data
    )

    db.add(session)
    db.commit()
    login_data["message"] = "Login successful"

    return login_data



@router.post("/logout")
def logout(session_token: str, db: Session = Depends(get_db)):
    session = db.query(SessionToken).filter(SessionToken.token == session_token).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    db.delete(session)
    db.commit()
    return {"message": "Logged out successfully"}



@router.get("/session")
def get_session_data(session_id: str = Header(...), db: Session = Depends(get_db)):
    session = db.query(SessionToken).filter(SessionToken.token == session_id).first()

    if not session or session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or expired session")


    decoded_json = base64.b64decode(session.encrypt_session_data.encode()).decode()
    session_data = json.loads(decoded_json)

    return session_data
