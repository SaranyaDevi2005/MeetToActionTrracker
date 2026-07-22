export default function AnalysisSection({ analysis }) {
  if (!analysis) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow mt-6">
      <h2 className="text-xl font-semibold mb-4">3. AI Analysis</h2>

      <div className="mb-4">
        <h3 className="font-semibold text-gray-700">Summary</h3>
        <p className="text-gray-800 mt-1">{analysis.summary}</p>
      </div>

      <div className="mb-4">
        <h3 className="font-semibold text-gray-700">Participants</h3>
        <div className="flex gap-2 flex-wrap mt-1">
          {analysis.participants?.map((p, i) => (
            <span key={i} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
              {p}
            </span>
          ))}
        </div>
      </div>

      <div>
        <h3 className="font-semibold text-gray-700">Decisions</h3>
        <ul className="list-disc list-inside mt-1 text-gray-800">
          {analysis.decisions?.map((d, i) => (
            <li key={i}>{d}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}