import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config.settings import settings


def send_task_email(to_email: str, task_title: str, deadline: str, meeting_name: str, owner_name: str):
    """Send a task assignment email via Gmail SMTP."""
    if not settings.GMAIL_ADDRESS or not settings.GMAIL_APP_PASSWORD:
        raise RuntimeError("Gmail credentials are not configured in .env")

    if not to_email:
        raise RuntimeError("No email address provided for this task owner")

    subject = f"New Task Assigned: {task_title}"
    body = f"""Hi {owner_name},

You have been assigned a new task from the meeting "{meeting_name}".

Task: {task_title}
Deadline: {deadline}

Please make sure to complete it on time.

- MeetingMind AI
"""

    msg = MIMEMultipart()
    msg["From"] = settings.GMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(settings.GMAIL_ADDRESS, settings.GMAIL_APP_PASSWORD)
        server.sendmail(settings.GMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
    except Exception as e:
        raise RuntimeError(f"Failed to send email: {str(e)}")