# app/api/v1/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models.ticket import Ticket as TicketModel, TicketStatus
from app.models.inventory import InventoryItem
from app.schemas.dashboard import (
    DashboardSummary,
    TicketStatusCounts,
    InventorySummary,
    SalesSummary,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    # ---- Tickets ----
    total_tickets = db.query(func.count(TicketModel.id)).scalar() or 0

    def count_status(status: TicketStatus) -> int:
        return (
            db.query(func.count(TicketModel.id))
            .filter(TicketModel.status == status)
            .scalar()
            or 0
        )

    backlog = count_status(TicketStatus.BACKLOG)
    to_do = count_status(TicketStatus.TO_DO)
    in_progress = count_status(TicketStatus.IN_PROGRESS)
    ready_for_shipment = count_status(TicketStatus.READY_FOR_SHIPMENT)
    out_for_delivery = count_status(TicketStatus.OUT_FOR_DELIVERY)
    delivered = count_status(TicketStatus.DELIVERED)

    tickets_summary = TicketStatusCounts(
        total=total_tickets,
        backlog=backlog,
        to_do=to_do,
        in_progress=in_progress,
        ready_for_shipment=ready_for_shipment,
        out_for_delivery=out_for_delivery,
        delivered=delivered,
    )

    # ---- Inventory ----
    item_count = db.query(func.count(InventoryItem.id)).scalar() or 0
    total_quantity = (
        db.query(func.coalesce(func.sum(InventoryItem.quantity), 0.0)).scalar() or 0.0
    )
    low_stock_count = (
        db.query(func.count(InventoryItem.id))
        .filter(
            InventoryItem.min_stock_alert.isnot(None),
            InventoryItem.min_stock_alert > 0,
            InventoryItem.quantity <= InventoryItem.min_stock_alert,
        )
        .scalar()
        or 0
    )

    inventory_summary = InventorySummary(
        item_count=item_count,
        total_quantity=float(total_quantity),
        low_stock_count=low_stock_count,
    )

    # ---- Sales ----
    total_revenue = (
        db.query(func.coalesce(func.sum(TicketModel.total_price), 0.0)).scalar() or 0.0
    )
    total_advance = (
        db.query(func.coalesce(func.sum(TicketModel.advance_paid), 0.0)).scalar()
        or 0.0
    )
    total_due = float(total_revenue) - float(total_advance)

    sales_summary = SalesSummary(
        total_revenue=float(total_revenue),
        total_advance=float(total_advance),
        total_due=float(total_due),
    )

    return DashboardSummary(
        tickets=tickets_summary,
        inventory=inventory_summary,
        sales=sales_summary,
    )
