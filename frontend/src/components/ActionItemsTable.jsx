import { useState } from "react";
import api from "../api";

export default function ActionItemsTable({ meetingId, actionItems, setActionItems }) {
  const [error, setError] = useState("");

  const updateField = (index, field, value) => {
    const updated = [...actionItems];
    updated[index][field] = value;
    setActionItems(updated);
  };

  const saveTask = async (index) => {
    const item = actionItems[index];
    try {
      await api.put("/task", {
        meeting_id: meetingId,
        task_index: index,
        owner: item.owner,
        task: item.task,
        deadline: item.deadline,
        approved: item.approved,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save task.");
    }
  };

  const toggleApprove = async (index) => {
    const updated = [...actionItems];
    updated[index].approved = !updated[index].approved;
    setActionItems(updated);
    await saveTask(index);
  };

  const deleteTask = async (index) => {
    try {
      await api.delete(`/task/${meetingId}/${index}`);
      const updated = actionItems.filter((_, i) => i !== index);
      setActionItems(updated);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to delete task.");
    }
  };

  const createCalendarEvent = async (index) => {
    setError("");
    try {
      const res = await api.post("/calendar/create", {
        meeting_id: meetingId,
        task_index: index,
      });
      const updated = [...actionItems];
      updated[index].calendar_event_id = "scheduled";
      setActionItems(updated);
      alert(`Reminders scheduled: ${res.data.reminders.join(", ")}`);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to schedule reminders.");
    }
  };

  if (!actionItems || actionItems.length === 0) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow mt-6">
      <h2 className="text-xl font-semibold mb-4">4. Action Items</h2>

      {error && <p className="text-red-600 mb-2">{error}</p>}

      <div className="overflow-x-auto">
        <table className="w-full text-sm border-collapse">
          <thead>
            <tr className="bg-gray-100 text-left">
              <th className="p-2 border">Owner</th>
              <th className="p-2 border">Task</th>
              <th className="p-2 border">Deadline</th>
              <th className="p-2 border">Approved</th>
              <th className="p-2 border">Calendar</th>
              <th className="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            {actionItems.map((item, index) => (
              <tr key={index} className="border-t">
                <td className="p-2 border">
                  <input
                    value={item.owner || ""}
                    onChange={(e) => updateField(index, "owner", e.target.value)}
                    onBlur={() => saveTask(index)}
                    className="w-full border rounded px-2 py-1"
                  />
                </td>
                <td className="p-2 border">
                  <input
                    value={item.task || ""}
                    onChange={(e) => updateField(index, "task", e.target.value)}
                    onBlur={() => saveTask(index)}
                    className="w-full border rounded px-2 py-1"
                  />
                </td>
                <td className="p-2 border">
                  <input
                    type="datetime-local"
                    value={item.deadline ? item.deadline.slice(0, 16) : ""}
                    onChange={(e) => updateField(index, "deadline", e.target.value)}
                    onBlur={() => saveTask(index)}
                    className="border rounded px-2 py-1"
                  />
                </td>
                <td className="p-2 border text-center">
                  <input
                    type="checkbox"
                    checked={item.approved || false}
                    onChange={() => toggleApprove(index)}
                  />
                </td>
                <td className="p-2 border text-center">
                  {item.calendar_event_id ? (
                    <span className="text-green-600 text-xs">✓ Reminders Scheduled</span>
                  ) : (
                    <button
                      onClick={() => createCalendarEvent(index)}
                      disabled={!item.approved}
                      className="bg-purple-600 text-white px-2 py-1 rounded text-xs disabled:opacity-40"
                    >
                      Schedule Remainders
                    </button>
                  )}
                </td>
                <td className="p-2 border text-center">
                  <button
                    onClick={() => deleteTask(index)}
                    className="text-red-600 hover:underline text-xs"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}