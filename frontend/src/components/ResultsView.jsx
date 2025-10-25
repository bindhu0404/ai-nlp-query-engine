import React from "react";

const ResultsView = ({ results, sql, error, loading, time }) => {
  // Don’t render anything if all states are empty
  if (!loading && !error && !sql && (!results || results.length === 0) && !time) {
    return null;
  }

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md">
      {loading && <p className="text-blue-600">Running query...</p>}

      {error && (
        <div className="text-red-600 font-semibold">
          ❌ {error}
        </div>
      )}

      {sql && (
        <div className="bg-gray-100 rounded-lg p-3 my-3 text-sm font-mono">
          <strong>Generated SQL:</strong>
          <pre className="whitespace-pre-wrap">{sql}</pre>
        </div>
      )}

      {results && results.length > 0 && (
        <div className="overflow-x-auto mt-4">
          <table className="min-w-full text-sm text-left border">
            <thead className="bg-gray-200">
              <tr>
                {Object.keys(results[0]).map((key) => (
                  <th key={key} className="px-4 py-2 border-b">{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {results.map((row, idx) => (
                <tr key={idx} className="hover:bg-gray-50">
                  {Object.values(row).map((val, i) => (
                    <td key={i} className="px-4 py-2 border-b">{String(val)}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {time > 0 && (
        <p className="text-gray-500 text-sm mt-3">⏱ Response Time: {time}s</p>
      )}
    </div>
  );
};

export default ResultsView;
