import React, { useState } from "react";

const DatabaseConnector = () => {
  const [connectionString, setConnectionString] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [schema, setSchema] = useState(null);

  const handleConnect = async () => {
    if (!connectionString.trim()) {
      setStatus("⚠️ Please enter a valid connection string.");
      return;
    }

    setLoading(true);
    setStatus("");
    setSchema(null);

    try {
      const formData = new FormData();
      formData.append("connection_string", connectionString);

      const res = await fetch("http://127.0.0.1:8000/api/ingest/database", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setLoading(false);

      if (res.ok) {
        setStatus("✅ Connection successful!");
        setSchema(data.schema || {});
      } else {
        setStatus(`❌ Failed: ${data.detail || "Could not connect"}`);
      }
    } catch (err) {
      setLoading(false);
      setStatus("❌ Backend connection error");
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md border border-gray-200">
      <h2 className="text-2xl font-semibold mb-4 text-blue-700">
        Database Connector
      </h2>

      <div className="flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          placeholder="postgresql://user:pass@host:port/dbname"
          value={connectionString}
          onChange={(e) => setConnectionString(e.target.value)}
          className="flex-1 border border-gray-300 rounded-xl px-4 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
        />
        <button
          onClick={handleConnect}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-xl transition disabled:opacity-50"
        >
          {loading ? "Connecting..." : "Connect"}
        </button>
      </div>

      {status && (
        <p
          className={`mt-3 font-medium ${
            status.includes("✅")
              ? "text-green-600"
              : status.includes("❌")
              ? "text-red-600"
              : "text-gray-700"
          }`}
        >
          {status}
        </p>
      )}

      {schema && (
        <div className="mt-5 bg-gray-100 rounded-lg p-4 text-sm">
          <h3 className="font-semibold text-gray-800 mb-2">
            Discovered Schema:
          </h3>
          <div className="space-y-1">
            {Object.keys(schema).map((table) => (
              <div key={table}>
                <strong className="text-gray-700">{table}</strong>:{" "}
                <span className="text-gray-600">
                  {schema[table].columns.map(c => c.name).join(", ")}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default DatabaseConnector;
