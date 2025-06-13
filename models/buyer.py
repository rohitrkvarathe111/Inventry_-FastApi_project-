from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Text, Float, BigInteger
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from database import Base
import datetime
from models.user_auth import User




class Bayer(Base):

    __tablename__ = "buyer"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    item_name = Column(String(150), nullable=False)
    item_quantity = Column(BigInteger, nullable=False)
    item_unit = Column(String(50), nullable=True)
    item_discription = Column(Text, nullable=True)
    item_manu_date = Column(DateTime, nullable=False)
    item_exp_date = Column(DateTime, nullable=False)
    item_pick_add = Column(String(100), nullable=True)
    item_pick_cords = Column(ARRAY(Float), nullable=True) 
    item_drop_add = Column(String(100), nullable=True)
    item_drop_cords = Column(ARRAY(Float), nullable=True) 

    