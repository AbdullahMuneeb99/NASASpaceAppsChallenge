// logbookAPI.js — client for Logbook backend routes

// BASE: API root. Keep empty for same-origin requests.
// If backend runs on a different port (e.g. Flask/Django dev), set accordingly.
const BASE = "http://localhost:8000";

/**
 * Helper: fetch JSON, throw on non-OK response.
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
 * LogbookAPI — wrapper for crew logbook routes.
 * Expected backend routes:
 *  GET    /logbook/entries
 *  POST   /logbook/entry       { author, content }
 *  DELETE /logbook/entry/:id
 */
export const LogbookAPI = {
  /** Fetch all logbook entries. */
  getEntries: () => jsonFetch(`${BASE}/logbook/entries`),

  /** Add a new logbook entry. */
  addEntry: (author, content) =>
    jsonFetch(`${BASE}/logbook/entry`, {
      method: "POST",
      body: JSON.stringify({ author, content }),
    }),

  /** Delete an entry by ID. */
  deleteEntry: (id) =>
    jsonFetch(`${BASE}/logbook/entry/${encodeURIComponent(id)}`, {
      method: "DELETE",
    }),
};
