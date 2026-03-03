from app.celery_app import celery_app
from pydantic import EmailStr
import asyncio
from aiosmtplib.errors import SMTPConnectError


@celery_app.task(
    name="send_message",
    bind=True,
    max_retries=None,
    retry_backoff=True,  # Экспоненциальная задержка,
    retry_backoff_max=16,
    # retry_jitter=True,
    autoretry_for=(SMTPConnectError,),
)
def send_message(self, subject: str, text: str, to: EmailStr):
    from app.services.messages import MessageService

    async def _send():
        await MessageService.send_email(subject=subject, text=text, to=to)

        return {
            "task_id": self.request.id,
            "processed": subject
        }

    return asyncio.run(_send())
