from app.celery_app import celery_app


@celery_app.task(name="send_message", bind=True)
def send_message(self, message_text: str):
    return {
        "task_id": self.request.id,
        "processed": message_text.upper()
    }
