from app.celery_app import celery_app
from pydantic import EmailStr
import asyncio
from aiosmtplib.errors import SMTPConnectError


@celery_app.task(
    name="send_one_message",
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


@celery_app.task(
    name="send_many_messages",
    bind=True,
    max_retries=None,
    retry_backoff=True,  # Экспоненциальная задержка,
    retry_backoff_max=16,
    # retry_jitter=True,
    autoretry_for=(SMTPConnectError,),
)
def send_messages(self, messages: list[dict]):
    from app.services.messages import MessageService

    async def _send():
        await MessageService.send_emails(messages=messages)

        return {
            "task_id": self.request.id,
            "processed": f"Sent {len(messages)} message{'s' if len(messages) > 1 else ''}",
        }

    return asyncio.run(_send())
