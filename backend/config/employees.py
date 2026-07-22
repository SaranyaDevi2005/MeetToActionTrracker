# Simple employee directory - map task owner names (as they appear in transcripts)
# to their real email addresses. Edit this with your actual test names/emails.

EMPLOYEES = {
    "john": "youremail1@gmail.com",
    "sarah": "youremail2@gmail.com",
    "raghul": "saranyadevi974@gmail.com",
    "priya": "71762233042@cit.edu.in",
}


def get_employee_email(owner_name: str) -> str | None:
    """Case-insensitive lookup of an employee's email by name."""
    if not owner_name:
        return None
    return EMPLOYEES.get(owner_name.strip().lower())