// src/apis/api.ts
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

console.log("API_BASE_URL =", API_BASE_URL);

export interface InventoryItem {
  id: number;
  name: string;
  code: string;
  category: string | null;
  unit: string;
  quantity: number;
  purchase_price: number | null;
  selling_price: number | null;
  min_stock_alert: number;
}

export interface InventoryCreateDto {
  name: string;
  code: string;
  category?: string | null;
  unit?: string;
  quantity?: number;
  purchase_price?: number | null;
  selling_price?: number | null;
  min_stock_alert?: number;
}

export interface TicketStatusCounts {
  total: number;
  backlog: number;
  to_do: number;
  in_progress: number;
  ready_for_shipment: number;
  out_for_delivery: number;
  delivered: number;
}

export interface InventorySummary {
  item_count: number;
  total_quantity: number;
  low_stock_count: number;
}

export interface SalesSummary {
  total_revenue: number;
  total_advance: number;
  total_due: number;
}

export interface DashboardSummary {
  tickets: TicketStatusCounts;
  inventory: InventorySummary;
  sales: SalesSummary;
}

export async function getDashboardSummary(): Promise<DashboardSummary> {
  const res = await fetch(`${API_BASE_URL}/dashboard/summary`);
  return handleResponse<DashboardSummary>(res);
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export async function getInventory(): Promise<InventoryItem[]> {
  const res = await fetch(`${API_BASE_URL}/inventory/`);
  return handleResponse<InventoryItem[]>(res);
}

export async function createInventory(
  payload: InventoryCreateDto
): Promise<InventoryItem> {
  const res = await fetch(`${API_BASE_URL}/inventory/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse<InventoryItem>(res);
}

export async function deleteInventory(id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/inventory/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Delete failed with status ${res.status}`);
  }
}
