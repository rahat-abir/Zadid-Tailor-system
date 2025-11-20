from sqlalchemy import Column, Integer, String, Float
from app.models.base import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(100), unique=True, index=True, nullable=False)
    category = Column(String(100), nullable=True)
    unit = Column(String(50), nullable=False, default="meter")  # meter/yard/gaz/piece
    quantity = Column(Float, nullable=False, default=0.0)
    purchase_price = Column(Float, nullable=True)
    selling_price = Column(Float, nullable=True)
    min_stock_alert = Column(Float, nullable=True, default=0.0)
