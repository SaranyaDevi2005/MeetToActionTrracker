import { useState } from "react";
import api from "../api";

export default function TranscriptSection({ meetingId, transcript, onAnalysisReady }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await api.post("/analyze", { meeting_id: meetingId, transcript });
      onAnalysisReady(res.data.analysis);
    } catch (err) {
      setError(err.response?.data?.detail || "Analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow mt-6">
      <h2 className="text-xl font-semibold mb-4">2. Transcript</h2>

      <div className="bg-gray-50 border rounded p-4 max-h-64 overflow-y-auto whitespace-pre-wrap text-sm">
        {transcript}
      </div>

      <button
        onClick={handleAnalyze}
        disabled={loading}
        className="bg-green-600 text-white px-4 py-2 rounded mt-4 hover:bg-green-700 disabled:opacity-50"
      >
        {loading ? "Analyzing..." : "Run AI Analysis"}
      </button>

      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}