import React, { useEffect, useState } from "react";
import { getVitals, simulateVitalChanges, getHealthStatus, getFirstAidProtocol } from "../services/medicalAPI";
import {MedicalAPI} from "../services/medicalAPI";

export default function MedicalTab() {
  const [vitals, setVitals] = useState(null);
  const [health, setHealth] = useState(null);
  const [firstAid, setFirstAid] = useState("");
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  /** Fetch all medical data */
  const fetchMedicalData = async () => {
    try {
      const [vitalsData, healthData, firstAidData] = await Promise.all([
        getVitals(),
        getHealthStatus(),
        getFirstAidProtocol(),
      ]);
      setVitals(vitalsData.data || vitalsData);
      setHealth(healthData.data || healthData);
      setFirstAid(firstAidData.data || firstAidData.text || "");
      setLoading(false);
    } catch (err) {
      console.error("Error fetching medical data:", err);
      setMessage("⚠ Failed to load medical data");
    }
  };

  /** Simulate changes in vitals */
  const handleSimulate = async () => {
    try {
      await simulateVitalChanges();
      setMessage("🫀 Simulating vital changes...");
      setTimeout(() => setMessage(""), 2000);
      fetchMedicalData();
    } catch (err) {
      console.error("Error simulating vitals:", err);
      setMessage("⚠ Failed to simulate vitals");
    }
  };

  useEffect(() => {
    fetchMedicalData();
    const interval = setInterval(handleSimulate, 10000); // auto-update every 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <p>Loading medical data...</p>;

  return (
    <div className="p-6 bg-gray-900 text-white rounded-2xl shadow-lg w-full max-w-xl mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-4 text-red-300">🩺 Medical Systems</h2>

      {message && <p className="text-sm text-cyan-400 mb-3">{message}</p>}

      {/* Vitals Section */}
      <div className="mb-6">
        <h3 className="text-xl mb-2 text-yellow-300">Vitals</h3>
        <ul className="space-y-1 text-lg">
          <li>
            ❤ Heart Rate:{" "}
            <span
              className={`font-semibold ${
                vitals.heart_rate > 100 || vitals.heart_rate < 60
                  ? "text-red-400"
                  : "text-green-400"
              }`}
            >
              {vitals.heart_rate} bpm
            </span>
          </li>
          <li>
            💉 Blood Pressure:{" "}
            <span
              className={`font-semibold ${
                vitals.bp_systolic > 140 || vitals.bp_diastolic > 90
                  ? "text-red-400"
                  : "text-green-400"
              }`}
            >
              {vitals.bp_systolic}/{vitals.bp_diastolic} mmHg
            </span>
          </li>
          <li>
            🌡 Temperature:{" "}
            <span
              className={`font-semibold ${
                vitals.temperature > 99.5 || vitals.temperature < 97
                  ? "text-red-400"
                  : "text-green-400"
              }`}
            >
              {vitals.temperature} °F
            </span>
          </li>
          <li className="text-gray-400 text-sm mt-1">
            Last updated: {vitals.timestamp || "—"}
          </li>
        </ul>
      </div>

      {/* Health Assessment */}
      <div className="mb-6">
        <h3 className="text-xl mb-2 text-green-300">🧬 Health Status</h3>
        <p
          className={`text-lg font-semibold ${
            health.status === "Critical"
              ? "text-red-400"
              : health.status === "Fair"
              ? "text-yellow-400"
              : "text-green-400"
          }`}
        >
          {health.status}
        </p>
        {health.recommendations && (
          <ul className="list-disc list-inside text-gray-300 mt-1">
            {health.recommendations.map((rec, i) => (
              <li key={i}>{rec}</li>
            ))}
          </ul>
        )}
      </div>

      {/* First Aid Section */}
      <div>
        <h3 className="text-xl mb-2 text-blue-300">🚑 First-Aid Protocol</h3>
        <div className="bg-gray-800 p-3 rounded-lg text-sm text-gray-200 whitespace-pre-wrap">
          {firstAid || "No protocol data available."}
        </div>
      </div>

      {/* Simulate Button */}
      <button
        onClick={handleSimulate}
        className="mt-6 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
      >
        Simulate Vital Changes
      </button>
    </div>
  );
}
