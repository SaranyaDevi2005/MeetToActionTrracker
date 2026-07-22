import { useState } from "react";
import api from "../api";

export default function UploadSection({ onTranscriptReady }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) {
      setError("Please choose an audio file first.");
      return;
    }
    setError("");
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await api.post("/upload-audio", formData);
      const meetingId = uploadRes.data.meeting_id;

      const transcribeRes = await api.post(`/transcribe?meeting_id=${meetingId}`);

      onTranscriptReady({
        meetingId,
        transcript: transcribeRes.data.transcript,
        meetingTitle: file.name,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Upload/transcription failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4">1. Upload Meeting Audio</h2>

      <input
        type="file"
        accept=".mp3,.wav,.m4a"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4 block"
      />

      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {loading ? "Processing..." : "Upload & Transcribe"}
      </button>

      {error && <p className="text-red-600 mt-2">{error}</p>}
    </div>
  );
}