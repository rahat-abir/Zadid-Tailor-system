// src/InventoryPage.tsx
import { useEffect, useState } from "react";
import type { InventoryItem, InventoryCreateDto } from "./apis/api";
import { getInventory, createInventory, deleteInventory } from "./apis/api";

const emptyForm: InventoryCreateDto = {
  name: "",
  code: "",
  category: "",
  unit: "meter",
  quantity: 0,
  purchase_price: undefined,
  selling_price: undefined,
  min_stock_alert: 0,
};

export function InventoryPage() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [form, setForm] = useState<InventoryCreateDto>(emptyForm);
  const [saving, setSaving] = useState(false);

  const loadItems = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getInventory();
      setItems(data);
    } catch (err: any) {
      setError(err.message || "Failed to load inventory");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadItems();
  }, []);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;

    if (["quantity", "purchase_price", "selling_price", "min_stock_alert"].includes(name)) {
      setForm((prev) => ({
        ...prev,
        [name]: value === "" ? undefined : Number(value),
      }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.name || !form.code) {
      setError("Name and Code are required");
      return;
    }
    try {
      setSaving(true);
      setError(null);
      await createInventory(form);
      setForm(emptyForm);
      await loadItems();
    } catch (err: any) {
      setError(err.message || "Failed to create item");
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this item?")) return;
    try {
      await deleteInventory(id);
      await loadItems();
    } catch (err: any) {
      setError(err.message || "Failed to delete item");
    }
  };

  return (
    <div className="app-container">
      <h1>Tailor Admin – Inventory</h1>

      <div className="layout">
        <section className="card">
          <h2>Add Inventory Item</h2>
          <form onSubmit={handleSubmit} className="form-grid">
            <label>
              Name*
              <input
                name="name"
                value={form.name ?? ""}
                onChange={handleChange}
                required
              />
            </label>
            <label>
              Code*
              <input
                name="code"
                value={form.code ?? ""}
                onChange={handleChange}
                required
              />
            </label>
            <label>
              Category
              <input
                name="category"
                value={form.category ?? ""}
                onChange={handleChange}
              />
            </label>
            <label>
              Unit
              <select name="unit" value={form.unit ?? ""} onChange={handleChange}>
                <option value="meter">meter</option>
                <option value="yard">yard</option>
                <option value="gaz">gaz</option>
                <option value="piece">piece</option>
              </select>
            </label>
            <label>
              Quantity
              <input
                type="number"
                name="quantity"
                value={form.quantity ?? 0}
                onChange={handleChange}
              />
            </label>
            <label>
              Purchase Price
              <input
                type="number"
                name="purchase_price"
                value={form.purchase_price ?? ""}
                onChange={handleChange}
              />
            </label>
            <label>
              Selling Price
              <input
                type="number"
                name="selling_price"
                value={form.selling_price ?? ""}
                onChange={handleChange}
              />
            </label>
            <label>
              Min Stock Alert
              <input
                type="number"
                name="min_stock_alert"
                value={form.min_stock_alert ?? 0}
                onChange={handleChange}
              />
            </label>

            <button type="submit" disabled={saving}>
              {saving ? "Saving..." : "Add Item"}
            </button>
          </form>

          {error && <p className="error">{error}</p>}
        </section>

        <section className="card">
          <h2>Inventory List</h2>
          {loading ? (
            <p>Loading...</p>
          ) : items.length === 0 ? (
            <p>No items yet.</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Code</th>
                  <th>Category</th>
                  <th>Unit</th>
                  <th>Qty</th>
                  <th>Selling</th>
                  <th>Min alert</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr
                    key={item.id}
                    className={
                      item.quantity <= item.min_stock_alert ? "low-stock" : ""
                    }
                  >
                    <td>{item.name}</td>
                    <td>{item.code}</td>
                    <td>{item.category}</td>
                    <td>{item.unit}</td>
                    <td>{item.quantity}</td>
                    <td>{item.selling_price ?? "-"}</td>
                    <td>{item.min_stock_alert}</td>
                    <td>
                      <button onClick={() => handleDelete(item.id)}>✕</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </section>
      </div>
    </div>
  );
}
