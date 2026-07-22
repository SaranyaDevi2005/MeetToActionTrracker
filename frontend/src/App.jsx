import { useState } from "react";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import MeetingPage from "./pages/MeetingPage";
import ChatPage from "./pages/ChatPage";

function App() {
  const [meetingId, setMeetingId] = useState(null);
  const [transcript, setTranscript] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [actionItems, setActionItems] = useState([]);

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow p-4 flex gap-6">
          <Link to="/" className="font-bold text-lg text-blue-600">MeetingMind AI</Link>
          <Link to="/" className="text-gray-700 hover:text-blue-600">Meeting</Link>
          <Link to="/chat" className="text-gray-700 hover:text-blue-600">AI Chat</Link>
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              <MeetingPage
                meetingId={meetingId}
                setMeetingId={setMeetingId}
                transcript={transcript}
                setTranscript={setTranscript}
                analysis={analysis}
                setAnalysis={setAnalysis}
                actionItems={actionItems}
                setActionItems={setActionItems}
              />
            }
          />
          <Route path="/chat" element={<ChatPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;