from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class InventryCreate(BaseModel):
    # user_id: int
    item_name: str = Field(..., max_length=150)
    item_total_quantity: int
    item_unit: Optional[str] = Field(None, max_length=50)
    item_price_per_unit: int
    item_discription: Optional[str] = None
    item_manu_date: datetime
    item_exp_date: datetime
    item_pick_add: Optional[str] = Field(None, max_length=100)
    item_pick_cords: Optional[List[float]] = None
    item_drop_add: Optional[str] = Field(None, max_length=100)
    item_drop_cords: Optional[List[float]] = None
    item_remaining_quantity: int

    class Config:
        orm_mode = True
