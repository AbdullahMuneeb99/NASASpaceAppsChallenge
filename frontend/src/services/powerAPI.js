// powerAPI.js — client for Power Systems backend routes

// BASE: API root. Leave empty for same-origin, or point to backend dev URL.
const BASE = "http://localhost:5000";


async function jsonFetch(url, opts = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.error || `HTTP ${res.status}`);
  return data;
}

export const PowerAPI = {
  /** Fetch current power status. */
  getStatus: () => jsonFetch(`${BASE}/power/status`),

  /** Simulate power usage (battery drain). */
  simulate: () =>
    jsonFetch(`${BASE}/power/simulate`, {
      method: "POST",
    }),

  /** Perform maintenance (restore battery, clear alerts). */
  maintain: () =>
    jsonFetch(`${BASE}/power/maintain`, {
      method: "POST",
    }),
};
