from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.ticket import Ticket as TicketModel, TicketStatus
from app.schemas.ticket import Ticket, TicketCreate, TicketUpdate

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/", response_model=List[Ticket])
def list_tickets(
    status: Optional[TicketStatus] = None,
    db: Session = Depends(get_db),
):
    query = db.query(TicketModel)
    if status:
        query = query.filter(TicketModel.status == status)
    return query.order_by(TicketModel.created_at.desc()).all()


@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_in: TicketCreate,
    db: Session = Depends(get_db),
):
    ticket = TicketModel(**ticket_in.model_dump())
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.get("/by-code/{ticket_code}", response_model=Ticket)
def get_ticket_by_code(ticket_code: str, db: Session = Depends(get_db)):
    ticket = (
        db.query(TicketModel)
        .filter(TicketModel.ticket_code == ticket_code)
        .first()
    )
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


@router.put("/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: int,
    ticket_in: TicketUpdate,
    db: Session = Depends(get_db),
):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    data = ticket_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(ticket, field, value)

    db.commit()
    db.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketModel).filter(TicketModel.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
    return
