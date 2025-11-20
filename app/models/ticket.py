import enum
import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SqlEnum

from app.models.base import Base


class TicketStatus(str, enum.Enum):
    BACKLOG = "backlog"
    TO_DO = "to_do"
    IN_PROGRESS = "in_progress"
    READY_FOR_SHIPMENT = "ready_for_shipment"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"


def generate_ticket_code() -> str:
    # simple unique code like: T-8CHAR
    return "T-" + uuid.uuid4().hex[:8].upper()


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_code = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
        default=generate_ticket_code,
    )

    customer_name = Column(String(255), nullable=False)
    customer_phone = Column(String(50), nullable=False)
    customer_address = Column(String(255), nullable=True)

    status = Column(
        SqlEnum(TicketStatus),
        nullable=False,
        default=TicketStatus.BACKLOG,
    )

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    due_date = Column(DateTime, nullable=True)

    total_price = Column(Float, nullable=True)
    advance_paid = Column(Float, nullable=True)
    payment_status = Column(String(50), nullable=True)  # unpaid/partial/paid
