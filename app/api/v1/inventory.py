from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.inventory import Inventory, InventoryCreate, InventoryUpdate
from app.models.inventory import InventoryItem
from app.api.deps import get_db

router = APIRouter(prefix="/inventory", tags=["inventory"])

@router.get("/", response_model=List[Inventory])
def list_inventory(db: Session = Depends(get_db)):
    items = db.query(InventoryItem).all()
    return items

@router.post("/", response_model=Inventory, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item_in: InventoryCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(InventoryItem)
        .filter(InventoryItem.code == item_in.code)
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Code already exists")

    item = InventoryItem(**item_in.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/{item_id}", response_model=Inventory)
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Inventory)
def update_inventory_item(
    item_id: int,
    item_in: InventoryUpdate,
    db: Session = Depends(get_db),
):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    data = item_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return
