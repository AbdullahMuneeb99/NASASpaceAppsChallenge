// frontend/src/components/LifeSupportTab.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { LifeSupportAPI } from "../services/lifeSupportAPI";

const LifeSupportTab = () => {
  const [lifeData, setLifeData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchLifeSupportData = async () => {
    try {
      const res = await axios.get("http://localhost:5000/life-support/status");
      setLifeData(res.data.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching life support data:", error);
    }
  };

  useEffect(() => {
    fetchLifeSupportData();
    const interval = setInterval(fetchLifeSupportData, 10000); // refresh every 10s
    return () => clearInterval(interval);
  }, []);

  if (loading) return <p>Loading life support data...</p>;

  return (
    <div className="p-6 bg-gray-900 text-white rounded-2xl shadow-lg w-full max-w-lg mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-4 text-cyan-300">
        🌿 Life Support Systems
      </h2>

      <div className="mb-3">
        <p className="text-lg">🫁 Oxygen Levels: {lifeData.oxygen_level}%</p>
        <div className="w-full bg-gray-700 rounded-full h-3 mt-1">
          <div
            className="h-3 rounded-full bg-cyan-400"
            style={{ width: `${lifeData.oxygen_level}%` }}
          ></div>
        </div>
      </div>

      <div className="mb-3">
        <p className="text-lg">💨 Air Pressure: {lifeData.air_pressure} kPa</p>
        <div className="w-full bg-gray-700 rounded-full h-3 mt-1">
          <div
            className="h-3 rounded-full bg-blue-400"
            style={{ width: `${(lifeData.air_pressure / 101) * 100}%` }}
          ></div>
        </div>
      </div>

      <div className="mb-3">
        <p className="text-lg">🚰 Portable Water Reserve: {lifeData.water_reserve}%</p>
        <div className="w-full bg-gray-700 rounded-full h-3 mt-1">
          <div
            className="h-3 rounded-full bg-green-400"
            style={{ width: `${lifeData.water_reserve}%` }}
          ></div>
        </div>
      </div>

      <h3 className="text-yellow-300 text-xl mt-4">System Notes</h3>
      {lifeData.alerts && lifeData.alerts.length > 0 ? (
        <ul className="list-disc list-inside mt-2 text-red-300">
          {lifeData.alerts.map((alert, idx) => (
            <li key={idx}>{alert}</li>
          ))}
        </ul>
      ) : (
        <p className="text-green-400 mt-2">All environmental systems stable ✅</p>
      )}
    </div>
  );
};

export default LifeSupportTab;
