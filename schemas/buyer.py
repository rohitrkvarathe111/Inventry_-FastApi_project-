from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

class ItemBuyer(BaseModel):

    item_id: int
    item_quantity: int

    class Config:
        from_attributes = True

