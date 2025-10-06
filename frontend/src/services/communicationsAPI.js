// API root. Keep empty for same-origin; set to "http://localhost:8000" if needed.
const BASE = "http://localhost:8000";

/** Send JSON and return parsed JSON (throws on non-2xx). */
async function jsonFetch(url, opts = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data?.error || `HTTP ${res.status}`);
  return data;
}

/** Communications API wrapper. Expects routes like:
 *  POST /comms/send        { sender, recipient, channel, content, type }
 *  GET  /comms/messages?channel=crew|earth|station
 *  GET  /comms/latest?channel=...
 *  POST /comms/clear       {}
 */
export const CommunicationsAPI = {
  sendMessage: (payload) =>
    jsonFetch(`${BASE}/comms/send`, { method: "POST", body: JSON.stringify(payload) }),

  getMessages: (channel = "") =>
    jsonFetch(`${BASE}/comms/messages${channel ? `?channel=${encodeURIComponent(channel)}` : ""}`),

  getLatest: (channel = "") =>
    jsonFetch(`${BASE}/comms/latest${channel ? `?channel=${encodeURIComponent(channel)}` : ""}`),

  clear: () => jsonFetch(`${BASE}/comms/clear`, { method: "POST", body: "{}" }),
};
