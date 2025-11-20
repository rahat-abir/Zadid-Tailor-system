from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TicketStatus(str, Enum):
    BACKLOG = "backlog"
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    READY_FOR_SHIPMENT = "ready_for_shipment"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"


class TicketBase(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: Optional[str] = None

    status: TicketStatus = TicketStatus.BACKLOG
    due_date: Optional[datetime] = None

    total_price: Optional[float] = None
    advance_paid: Optional[float] = None
    payment_status: Optional[str] = None  # unpaid/partial/paid


class TicketCreate(TicketBase):
    # ticket_code will be auto-generated in DB
    pass


class TicketUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None

    status: Optional[TicketStatus] = None
    due_date: Optional[datetime] = None

    total_price: Optional[float] = None
    advance_paid: Optional[float] = None
    payment_status: Optional[str] = None


class Ticket(TicketBase):
    id: int
    ticket_code: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
