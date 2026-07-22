import datetime
from urllib.parse import quote

def create_calendar_event(task_title: str, deadline: str, description: str, meeting_name: str) -> str:
    """
    Generate a Google Calendar 'quick add' link instead of using the API.
    No OAuth/billing needed - user just clicks the link and saves the event.
    """
    try:
        start_time = datetime.datetime.fromisoformat(deadline)
        end_time = start_time + datetime.timedelta(minutes=30)

        # Google Calendar expects UTC format: YYYYMMDDTHHMMSSZ
        start_str = start_time.strftime("%Y%m%dT%H%M%S")
        end_str = end_time.strftime("%Y%m%dT%H%M%S")

        full_description = f"{description}\n\nMeeting: {meeting_name}"

        base_url = "https://calendar.google.com/calendar/render"
        params = (
            f"?action=TEMPLATE"
            f"&text={quote(task_title)}"
            f"&dates={start_str}/{end_str}"
            f"&details={quote(full_description)}"
        )

        return base_url + params
    except Exception as e:
        raise RuntimeError(f"Calendar link generation failed: {str(e)}")