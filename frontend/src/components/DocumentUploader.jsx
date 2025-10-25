import React, { useState } from "react";

const DocumentUploader = () => {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    setFiles([...e.target.files]);
    setStatus("");
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setStatus("⚠️ Please select files to upload.");
      return;
    }

    setUploading(true);
    setStatus("Uploading...");

    const formData = new FormData();
    files.forEach((file) => formData.append("files", file));

    try {
      const res = await fetch("http://127.0.0.1:8000/api/ingest/documents", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setUploading(false);

      if (res.ok) {
        setStatus(`✅ ${data.message || "Documents uploaded successfully!"}`);
      } else {
        setStatus(`❌ Upload failed: ${data.error || "Unknown error"}`);
      }
    } catch (err) {
      setUploading(false);
      setStatus("❌ Backend connection error");
    }
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-md border border-gray-200">
      <h2 className="text-2xl font-semibold mb-4 text-green-700">
        Document Uploader
      </h2>

      <div className="flex flex-col sm:flex-row gap-4 items-center">
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 
                     file:rounded-full file:border-0 file:text-sm file:font-semibold
                     file:bg-green-100 file:text-green-700 hover:file:bg-green-200"
        />
        <button
          onClick={handleUpload}
          disabled={uploading}
          className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-xl transition disabled:opacity-50"
        >
          {uploading ? "Uploading..." : "Upload"}
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

      {files.length > 0 && (
        <div className="mt-4 bg-gray-50 rounded-lg p-3 text-sm text-gray-700">
          <h4 className="font-semibold mb-2">Selected Files:</h4>
          <ul className="space-y-1">
            {files.map((f, i) => (
              <li key={i}>📄 {f.name}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default DocumentUploader;
