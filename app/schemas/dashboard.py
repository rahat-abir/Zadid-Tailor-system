# app/schemas/dashboard.py
from pydantic import BaseModel
from typing import Optional


class TicketStatusCounts(BaseModel):
    total: int
    backlog: int
    to_do: int
    in_progress: int
    ready_for_shipment: int
    out_for_delivery: int
    delivered: int


class InventorySummary(BaseModel):
    item_count: int
    total_quantity: float
    low_stock_count: int


class SalesSummary(BaseModel):
    total_revenue: float
    total_advance: float
    total_due: float


class DashboardSummary(BaseModel):
    tickets: TicketStatusCounts
    inventory: InventorySummary
    sales: SalesSummary
