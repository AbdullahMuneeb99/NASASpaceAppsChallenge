import React, { useEffect, useState } from "react";
import { LogbookAPI } from "../services/logbookAPI";

export default function LogbookTab() {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [author, setAuthor] = useState("Astronaut A");
  const [content, setContent] = useState("");
  const [msg, setMsg] = useState("");

  // fetch all logbook entries
  const fetchEntries = async () => {
    try {
      const data = await LogbookAPI.getEntries();
      setEntries(data.items || data || []);
      setLoading(false);
    } catch (err) {
      console.error("Error fetching logbook entries:", err);
      setMsg("⚠️ Failed to load logbook entries");
    }
  };

  // add a new log entry
  const addEntry = async () => {
    if (!content.trim()) {
      setMsg("Entry content required");
      return;
    }
    try {
      await LogbookAPI.addEntry(author, content);
      setMsg("✅ Entry added");
      setContent("");
      fetchEntries();
    } catch (err) {
      console.error("Error adding logbook entry:", err);
      setMsg("⚠️ Failed to add entry");
    }
  };

  // delete an entry
  const deleteEntry = async (id) => {
    try {
      await LogbookAPI.deleteEntry(id);
      setMsg("🗑️ Entry deleted");
      fetchEntries();
    } catch (err) {
      console.error("Error deleting entry:", err);
      setMsg("⚠️ Failed to delete entry");
    }
  };

  useEffect(() => {
    fetchEntries();
  }, []);

  if (loading) return <p>Loading logbook...</p>;

  return (
    <div className="p-6 bg-gray-900 text-white rounded-2xl shadow-lg w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-2xl font-semibold mb-4 text-yellow-300">📓 Crew Logbook</h2>
      {msg && <p className="text-sm text-cyan-400 mb-2">{msg}</p>}

      {/* New entry form */}
      <div className="mb-6">
        <input
          type="text"
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          placeholder="Author"
          className="w-full mb-2 p-2 rounded bg-gray-800 text-white"
        />
        <textarea
          rows={3}
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write log entry..."
          className="w-full p-2 rounded bg-gray-800 text-white"
        />
        <button
          onClick={addEntry}
          className="mt-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg"
        >
          Add Entry
        </button>
      </div>

      {/* Logbook entries */}
      <h3 className="text-xl mb-2 text-green-300">Entries</h3>
      <ul className="space-y-3">
        {entries.length ? (
          entries.map((e) => (
            <li
              key={e.id}
              className="p-3 bg-gray-800 rounded-lg flex justify-between items-start"
            >
              <div>
                <p className="text-sm text-gray-400">
                  {e.timestamp || "—"} — <b>{e.author}</b>
                </p>
                <p>{e.content}</p>
              </div>
              <button
                onClick={() => deleteEntry(e.id)}
                className="ml-3 text-red-400 hover:text-red-600"
              >
                ✖
              </button>
            </li>
          ))
        ) : (
          <li className="text-gray-400">No log entries yet</li>
        )}
      </ul>
    </div>
  );
}
