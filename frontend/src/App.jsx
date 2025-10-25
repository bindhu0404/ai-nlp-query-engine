import React, { useState } from "react";
import Header from "./components/Header";
import QueryPanel from "./components/QueryPanel";
import ResultsView from "./components/ResultsView";
import DatabaseConnector from "./components/DatabaseConnector";
import DocumentUploader from "./components/DocumentUploader";

const App = () => {
  const [results, setResults] = useState(null);
  const [sql, setSql] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [time, setTime] = useState(0);

  const handleQuery = async (query) => {
    setLoading(true);
    setError("");
    setResults(null);
    setSql("");
    try {
      const res = await fetch("http://127.0.0.1:8000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setLoading(false);
      setTime(data.response_time);

      if (data.error) {
        setError(data.error);
        setSql(data.generated_sql || "");
      } else {
        setSql(data.generated_sql);
        setResults(data.results);
      }
    } catch (err) {
      setLoading(false);
      setError("Unable to connect to backend.");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-4">
      <Header />

      <div className="max-w-5xl mx-auto mt-6 space-y-6">
        {/* Step 1: Connect to DB */}
        <DatabaseConnector />

        {/* Step 2: Upload Documents */}
        <DocumentUploader />

        {/* Step 3: Query Section */}
        <QueryPanel onSubmit={handleQuery} loading={loading} />

        {/* Step 4: Results */}
        <ResultsView
          results={results}
          sql={sql}
          error={error}
          loading={loading}
          time={time}
        />
      </div>
    </div>
  );
};

export default App;
