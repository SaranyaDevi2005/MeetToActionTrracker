from apscheduler.schedulers.background import BackgroundScheduler
import datetime

from services.email_service import send_task_email

scheduler = BackgroundScheduler()
scheduler.start()


def schedule_task_reminders(owner_email: str, task_title: str, deadline: str, meeting_name: str, owner_name: str):
    """Schedule two reminder emails: 24 hours before and 30 minutes before the deadline."""
    if not owner_email:
        raise RuntimeError("No email address available for this task owner")

    deadline_dt = datetime.datetime.fromisoformat(deadline)
    now = datetime.datetime.now()

    reminder_24h = deadline_dt - datetime.timedelta(hours=24)
    reminder_30m = deadline_dt - datetime.timedelta(minutes=30)

    jobs_scheduled = []

    if reminder_24h > now:
        scheduler.add_job(
            send_task_email,
            "date",
            run_date=reminder_24h,
            args=[owner_email, task_title, deadline, meeting_name, owner_name],
        )
        jobs_scheduled.append("24-hour reminder")

    if reminder_30m > now:
        scheduler.add_job(
            send_task_email,
            "date",
            run_date=reminder_30m,
            args=[owner_email, task_title, deadline, meeting_name, owner_name],
        )
        jobs_scheduled.append("30-minute reminder")

    if not jobs_scheduled:
        # deadline is too close/past - send an immediate notification instead
        send_task_email(owner_email, task_title, deadline, meeting_name, owner_name)
        jobs_scheduled.append("immediate (deadline too close for scheduled reminders)")

    return jobs_scheduled