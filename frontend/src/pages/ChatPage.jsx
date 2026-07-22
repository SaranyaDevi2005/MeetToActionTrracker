import { useState } from "react";
import api from "../api";

export default function ChatPage() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);
    setQuery("");
    setError("");
    setLoading(true);

    try {
      const res = await api.post("/chat", { query: userMessage.text });
      setMessages((prev) => [...prev, { role: "ai", text: res.data.answer }]);
    } catch (err) {
      setError(err.response?.data?.detail || "Chat failed.");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleAsk();
  };

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">AI Chat — Ask About Past Meetings</h1>

      <div className="bg-white rounded-lg shadow p-4 h-96 overflow-y-auto mb-4">
        {messages.length === 0 && (
        <p className="text-gray-400">Ask something like &quot;Who is responsible for the payment API?&quot;</p>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`mb-3 p-3 rounded max-w-[80%] ${
              msg.role === "user"
                ? "bg-blue-600 text-white ml-auto"
                : "bg-gray-100 text-gray-800"
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && <p className="text-gray-400">Thinking...</p>}
      </div>

      {error && <p className="text-red-600 mb-2">{error}</p>}

      <div className="flex gap-2">
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your question..."
          className="flex-1 border rounded px-4 py-2"
        />
        <button
          onClick={handleAsk}
          className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
        >
          Ask
        </button>
      </div>
    </div>
  );
}