# Simple in-memory storage (no MongoDB needed)
# Data is lost when the server restarts - fine for testing/demo purposes

meetings_store = {}  # meeting_id -> meeting dict
calendar_events_store = []  # list of calendar event dicts


class MeetingsCollection:
    def insert_one(self, doc):
        meetings_store[doc["meeting_id"]] = doc

    def find_one(self, query):
        meeting_id = query.get("meeting_id")
        return meetings_store.get(meeting_id)

    def update_one(self, query, update):
        meeting_id = query.get("meeting_id")
        if meeting_id in meetings_store:
            meetings_store[meeting_id].update(update["$set"])

    def find(self, query=None):
        query = query or {}
        results = list(meetings_store.values())
        if "title" in query:
            search_term = query["title"]["$regex"].lower()
            results = [m for m in results if search_term in m.get("title", "").lower()]
        return SortableList(results)


class SortableList(list):
    def sort(self, field, direction=-1):
        self_copy = sorted(self, key=lambda x: x.get(field, ""), reverse=(direction == -1))
        self.clear()
        self.extend(self_copy)
        return self


class CalendarEventsCollection:
    def insert_one(self, doc):
        calendar_events_store.append(doc)


meetings_collection = MeetingsCollection()
calendar_events_collection = CalendarEventsCollection()