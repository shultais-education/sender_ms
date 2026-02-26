from app.celery_app import celery_app
import asyncio


@celery_app.task(
    name="send_message",
    bind=True,
    max_retries=None,
    retry_backoff=True,  # Экспоненциальная задержка,
    retry_backoff_max=16,
    # retry_jitter=True,
    autoretry_for=(ValueError,),
)
def send_message(self, message_text: str):
    from app.services.messages import MessageService

    async def _send():
        await MessageService.send_email(to="nikita@shultais.ru", subject="Новое сообщение", body=message_text)

        return {
            "task_id": self.request.id,
            "processed": message_text.upper()
        }

    return asyncio.run(_send())
