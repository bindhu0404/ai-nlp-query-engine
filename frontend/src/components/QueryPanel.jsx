// frontend/src/components/QueryPanel.jsx
import React, { useState, useEffect } from "react";

const QueryPanel = ({ onSubmit, loading }) => {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState([]);

  // Fetch query history on mount
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/query/history");
        if (res.ok) {
          const data = await res.json();
          setHistory(data.history.reverse()); // latest first
        }
      } catch (err) {
        console.error("Failed to fetch query history", err);
      }
    };
    fetchHistory();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  const handleSelectHistory = (q) => {
    setQuery(q);
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md">
      <h2 className="text-xl font-semibold mb-3">Natural Language Query</h2>

      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <input
          type="text"
          placeholder='e.g. "List all employees in Engineering earning above 70k"'
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 border border-gray-300 rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-xl disabled:opacity-50"
        >
          {loading ? "Processing..." : "Run Query"}
        </button>
      </form>

      {history.length > 0 && (
        <div className="mt-4 bg-gray-100 p-3 rounded-lg text-sm">
          <h3 className="font-semibold mb-2">Previous Queries:</h3>
          <ul className="space-y-1">
            {history.map((h, idx) => (
              <li
                key={idx}
                className="cursor-pointer text-blue-600 hover:underline"
                onClick={() => handleSelectHistory(h.query)}
              >
                {h.query}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default QueryPanel;
