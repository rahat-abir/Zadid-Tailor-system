from pydantic import BaseModel, ConfigDict
from typing import Optional

class InventoryBase(BaseModel):
    name: str
    code: str
    category: Optional[str] = None
    unit: str = "meter"
    quantity: float = 0.0
    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None
    min_stock_alert: float = 0.0

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None
    quantity: Optional[float] = None
    purchase_price: Optional[float] = None
    selling_price: Optional[float] = None
    min_stock_alert: Optional[float] = None

class Inventory(InventoryBase):
    id: int
    # This is the Pydantic v2 replacement for orm_mode = True
    model_config = ConfigDict(from_attributes=True)
