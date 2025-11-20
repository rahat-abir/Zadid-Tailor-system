// src/DashboardPage.tsx
import { useEffect, useState } from "react";
import type { DashboardSummary } from "./apis/api";
import { getDashboardSummary } from "./apis/api";

export function DashboardPage() {
  const [data, setData] = useState<DashboardSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const res = await getDashboardSummary();
        setData(res);
      } catch (err: any) {
        setError(err.message ?? "Failed to load dashboard");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <div className="app-container">
      <h1>Dashboard</h1>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      {data && !loading && !error && (
        <div className="dashboard-grid">
          {/* Tickets */}
          <section className="card">
            <h2>Tickets</h2>
            <div className="dashboard-stat-main">
              <span className="stat-label">Total tickets</span>
              <span className="stat-value">{data.tickets.total}</span>
            </div>

            <div className="status-chips">
              <div className="chip">
                <span>Backlog</span>
                <strong>{data.tickets.backlog}</strong>
              </div>
              <div className="chip">
                <span>To do</span>
                <strong>{data.tickets.to_do}</strong>
              </div>
              <div className="chip">
                <span>In progress</span>
                <strong>{data.tickets.in_progress}</strong>
              </div>
              <div className="chip">
                <span>Ready to ship</span>
                <strong>{data.tickets.ready_for_shipment}</strong>
              </div>
              <div className="chip">
                <span>Out for delivery</span>
                <strong>{data.tickets.out_for_delivery}</strong>
              </div>
              <div className="chip">
                <span>Delivered</span>
                <strong>{data.tickets.delivered}</strong>
              </div>
            </div>
          </section>

          {/* Inventory */}
          <section className="card">
            <h2>Inventory</h2>
            <div className="dashboard-stat-main">
              <span className="stat-label">Distinct items</span>
              <span className="stat-value">{data.inventory.item_count}</span>
            </div>
            <div className="dashboard-kv">
              <span>Total quantity</span>
              <strong>{data.inventory.total_quantity.toFixed(2)}</strong>
            </div>
            <div className="dashboard-kv">
              <span>Low stock items</span>
              <strong>{data.inventory.low_stock_count}</strong>
            </div>
          </section>

          {/* Sales */}
          <section className="card">
            <h2>Sales</h2>
            <div className="dashboard-stat-main">
              <span className="stat-label">Total revenue</span>
              <span className="stat-value">
                {data.sales.total_revenue.toFixed(2)}
              </span>
            </div>
            <div className="dashboard-kv">
              <span>Advance received</span>
              <strong>{data.sales.total_advance.toFixed(2)}</strong>
            </div>
            <div className="dashboard-kv">
              <span>Due</span>
              <strong>{data.sales.total_due.toFixed(2)}</strong>
            </div>
          </section>
        </div>
      )}
    </div>
  );
}
