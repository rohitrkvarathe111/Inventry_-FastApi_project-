from sqlalchemy.orm import relationship
from database import Base

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Float, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY
import datetime
from datetime import timedelta


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    mobile_number = Column(String(13), nullable=True)  

    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    created_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    update_by = Column(Integer, ForeignKey('users.id'), nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Optional: Self-referential relationships
    creator = relationship("User", remote_side=[id], foreign_keys=[created_by], post_update=True, backref="created_users")
    updater = relationship("User", remote_side=[id], foreign_keys=[update_by], post_update=True, backref="updated_users")
    inventories = relationship("Inventry", back_populates="user", foreign_keys="[Inventry.user_id]")



class SessionToken(Base):
    __tablename__ = "session_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, index=True, nullable=False)
    encrypt_session_data = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    expires_at = Column(DateTime)

    user = relationship("User")




# class Inventry(Base):
#     __tablename__ = "inventry"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, ForeignKey('users.username'), nullable=False)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

#     item_name = Column(String(150), nullable=False)
#     item_total_quantity = Column(BigInteger, nullable=False)
#     item_unit = Column(String(50), nullable=True)
#     item_price_per_unit = Column(BigInteger, nullable=False)
#     item_discription = Column(Text, nullable=True)
#     item_manu_date = Column(DateTime, nullable=False)
#     item_exp_date = Column(DateTime, nullable=False)
#     item_pick_add = Column(String(100), nullable=True)
#     item_pick_cords = Column(ARRAY(Float), nullable=True) 
#     item_drop_add = Column(String(100), nullable=True)
#     item_drop_cords = Column(ARRAY(Float), nullable=True)
#     item_remaining_quantity = Column(BigInteger, nullable=False) 


#     created_at = Column(DateTime, default=datetime.datetime.utcnow)
#     updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
#     is_deleted = Column(Boolean, default=True)
