// lifesupportAPI.js
/** Base path for the Flask routes (adjust if your server differs). */
const BASE_URL = "http://localhost:8000";

/** Helper to call the API and parse JSON, with friendly errors. */
async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: options.method || 'GET',
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const text = await res.text(); // handle empty bodies safely
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) {
    const msg = (data && (data.error || data.message)) || `HTTP ${res.status}`;
    throw new Error(`LifeSupportAPI: ${msg}`);
  }
  return data;
}

/** Get current life-support status (oxygen, pressure, water, alerts). */
export function getStatus() {
  return request('/status');
}

/** Simulate environment changes (random drift + leak chance). */
export function simulateEnvironment() {
  return request('/simulate', { method: 'POST' });
}

/** Refill water reserves to 100%. */
export function refillWater() {
  return request('/refill-water', { method: 'POST' });
}

/** Repair a detected leak (no-op if none). */
export function repairLeak() {
  return request('/repair-leak', { method: 'POST' });
}

/** Optional default export for convenience. */
export default { getStatus, simulateEnvironment, refillWater, repairLeak };
