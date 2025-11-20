import { useState } from "react";
import "./App.css";
import { InventoryPage } from "./InventoryPage";
import { DashboardPage } from "./DashboardPage";

type View = "dashboard" | "inventory";

function App() {
  const [view, setView] = useState<View>("dashboard");

  return (
    <>
      <div className="top-nav">
        <div className="top-nav-title">Tailor Admin</div>
        <div className="top-nav-tabs">
          <button
            className={
              view === "dashboard" ? "nav-btn active" : "nav-btn"
            }
            onClick={() => setView("dashboard")}
          >
            Dashboard
          </button>
          <button
            className={
              view === "inventory" ? "nav-btn active" : "nav-btn"
            }
            onClick={() => setView("inventory")}
          >
            Inventory
          </button>
        </div>
      </div>

      {view === "dashboard" ? <DashboardPage /> : <InventoryPage />}
    </>
  );
}

export default App;
