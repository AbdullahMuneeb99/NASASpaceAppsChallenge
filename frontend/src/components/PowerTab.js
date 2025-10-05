// frontend/src/components/PowerTab.js
import React, { useState, useEffect } from "react";
import axios from "axios";

const PowerTab = () => {
  const [powerData, setPowerData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const fetchPowerStatus = async () => {
    try {
      const res = await axios.get("http://localhost:5000/power/status");
      setPowerData(res.data.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching power status:", error);
    }
  };

  const simulatePowerUsage = async () => {
    try {
      const res = await axios.post("http://localhost:5000/power/simulate");
      setPowerData(res.data.data);
      setMessage("⚙️ Simulated power usage");
      setTimeout(() => setMessage(""), 2000);
    } catch (error) {
      console.error("Error simulating power usage:", error);
    }
  };

  const performMaintenance = async () => {
    try {
      const res = await axios.post("http://localhost:5000/power/maintain");
      setPowerData((prev) => ({
        ...prev,
        battery_level: 100,
        backup_battery_ready: true,
        maintenance_alerts: [],
      }));
      setMessage(res.data.data.message);
      setTimeout(() => setMessage(""), 3000);
    } catch (error) {
      console.error("Error performing maintenance:", error);
    }
  };

  useEffect(() => {
    fetchPowerStatus();
    const interval = setInterval(simulatePowerUsage, 10000); // auto-simulate every 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <p>Loading power data...</p>;

  return (
    <div className="p-6 bg-gray-900 text-white rounded-2xl shadow-lg w-full max-w-lg mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-4 text-blue-300">⚡ Power Systems</h2>

      <div className="mb-4">
        <p className="text-lg">
          🔋 Battery Level:{" "}
          <span
            className={`font-bold ${
              powerData.battery_level < 25 ? "text-red-400" : "text-green-400"
            }`}
          >
            {powerData.battery_level}%
          </span>
        </p>
        <div className="w-full bg-gray-700 rounded-full h-3 mt-1">
          <div
            className="h-3 rounded-full bg-green-400"
            style={{ width: `${powerData.battery_level}%` }}
          ></div>
        </div>
      </div>

      <p className="mb-2">
        🪫 Backup Battery:{" "}
        <span
          className={
            powerData.backup_battery_ready ? "text-green-400" : "text-red-400"
          }
        >
          {powerData.backup_battery_ready ? "Ready" : "Offline"}
        </span>
      </p>

      <h3 className="text-xl mt-4 text-yellow-300">🧰 Maintenance Alerts</h3>
      {powerData.maintenance_alerts.length > 0 ? (
        <ul className="list-disc list-inside mt-2 text-red-300">
          {powerData.maintenance_alerts.map((alert, index) => (
            <li key={index}>{alert}</li>
          ))}
        </ul>
      ) : (
        <p className="text-green-400 mt-2">All systems nominal ✅</p>
      )}

      <div className="flex justify-between mt-6">
        <button
          onClick={simulatePowerUsage}
          className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
        >
          Simulate Usage
        </button>
        <button
          onClick={performMaintenance}
          className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg"
        >
          Perform Maintenance
        </button>
      </div>

      {message && <p className="mt-4 text-sm text-yellow-400">{message}</p>}
    </div>
  );
};

export default PowerTab;
