from pydantic import BaseModel, Field, validator
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
        from_attributes = True


# class ItemRequest(BaseModel):
#     id: int


class ItemResponse(BaseModel):
    id: int
    item_name: str
    item_unit: str
    item_total_quantity: int

    class Config:
        from_attributes = True
        

class AllItemResponse(BaseModel):
    id: int
    item_name: str
    item_remaining_quantity: int
    item_exp_date: str

    @validator("item_exp_date", pre=True)
    def format_exp_date(cls, v):
        if isinstance(v, datetime):
            return v.strftime("%d-%m-%Y %H:%M:%S")
        return v


    class Config:
        orm_mode = True