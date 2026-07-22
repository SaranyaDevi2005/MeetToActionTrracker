import UploadSection from "../components/UploadSection";
import TranscriptSection from "../components/TranscriptSection";
import AnalysisSection from "../components/AnalysisSection";
import ActionItemsTable from "../components/ActionItemsTable";

export default function MeetingPage({
  meetingId,
  setMeetingId,
  transcript,
  setTranscript,
  analysis,
  setAnalysis,
  actionItems,
  setActionItems,
}) {
  const handleTranscriptReady = ({ meetingId, transcript }) => {
    setMeetingId(meetingId);
    setTranscript(transcript);
    setAnalysis(null);
    setActionItems([]);
  };

  const handleAnalysisReady = (analysisData) => {
    setAnalysis(analysisData);
    setActionItems(analysisData.action_items || []);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">Meeting Notes & Action Tracker</h1>

      <UploadSection onTranscriptReady={handleTranscriptReady} />

      {transcript && (
        <TranscriptSection
          meetingId={meetingId}
          transcript={transcript}
          onAnalysisReady={handleAnalysisReady}
        />
      )}

      {analysis && <AnalysisSection analysis={analysis} />}

      {actionItems.length > 0 && (
        <ActionItemsTable
          meetingId={meetingId}
          actionItems={actionItems}
          setActionItems={setActionItems}
        />
      )}
    </div>
  );
}