// medicalAPI.js
/** Adjust if your Flask route prefix differs. */
const BASE_URL = '/api/medical';

/** Tiny fetch helper with JSON parsing + friendly errors. */
async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: options.method || 'GET',
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;
  if (!res.ok) {
    const msg = (data && (data.error || data.message)) || `HTTP ${res.status}`;
    throw new Error(`MedicalAPI: ${msg}`);
  }
  return data;
}

/** Get the latest vital readings (HR, BP, temperature, timestamp). */
export function getVitals() {
  return request('/vitals');
}

/** Trigger random vital changes for testing/animations. */
export function simulateVitalChanges() {
  return request('/simulate', { method: 'POST' });
}

/** Get a simple health assessment based on current vitals. */
export function getHealthStatus() {
  return request('/status');
}

/** Fetch the First-Aid protocol text bundle. */
export function getFirstAidProtocol() {
  return request('/first-aid');
}

export default { getVitals, simulateVitalChanges, getHealthStatus, getFirstAidProtocol };
