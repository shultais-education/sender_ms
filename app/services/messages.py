from app.schemas.message import TaskResponse
from app.tasks import send_message as send_message_task
from app.core.config import settings
import aiosmtplib
from email.mime.text import MIMEText


class MessageService:

    @staticmethod
    async def send_message(message: str, delay: int = 0) -> TaskResponse:
        task = send_message_task.apply_async(args=[message], countdown=delay)

        return TaskResponse(
            task_id=task.task_id,
            status="PENDING",
            message="Задача успешно поставлена в очередь"
        )

    @staticmethod
    async def send_email(to: str, subject: str, body: str):
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "noreply@localhost"
        msg["To"] = to

        async with aiosmtplib.SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT) as smtp:
            await smtp.send_message(msg)

