from app.celery_app import celery_app


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

    # raise ValueError("Test error")

    return {
        "task_id": self.request.id,
        "processed": message_text.upper()
    }
