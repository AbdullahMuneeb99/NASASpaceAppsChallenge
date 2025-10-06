// sleepAPI.js — client for the Django routes (same-origin)

// BASE: API root. Keep empty for same-origin requests.
const BASE = "http://localhost:8000"; // or "http://localhost:8000" if Django runs separately

/**
 * Helper to send a JSON fetch request and return parsed data.
 * Throws an error if the response status is not OK.
 */
async function jsonFetch(url, opts = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.error || `HTTP ${res.status}`);
  return data;
}

/**
 * SleepAPI — small wrapper for all sleep endpoints.
 * Each function talks to the Django backend and returns JSON.
 */
export const SleepAPI = {
  /** Add a new sleep log entry (bed and wake times). */
  addLog: async (bed, wake) =>
    jsonFetch(`${BASE}/sleep/add`, {
      method: "POST",
      body: JSON.stringify({ bed, wake }),
    }),

  /** Get the most recent sleep logs (default 5). */
  getRecent: async (n = 5) =>
    jsonFetch(`${BASE}/sleep/recent?n=${encodeURIComponent(n)}`),

  /** Get the average sleep duration over the last k logs (default 7). */
  getAverage: async (k = 7) =>
    jsonFetch(`${BASE}/sleep/average?k=${encodeURIComponent(k)}`),

  /** Plan an alarm set X minutes from now. */
  planAlarm: async (minutes) =>
    jsonFetch(`${BASE}/alarm/plan`, {
      method: "POST",
      body: JSON.stringify({ minutes }),
    }),
};
