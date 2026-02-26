from app.schemas.message import TaskResponse
from app.tasks import send_message as send_message_task


class MessageService:

    @staticmethod
    async def send_message(message: str, delay: int = 0) -> TaskResponse:
        task = send_message_task.apply_async(args=[message], countdown=delay)

        return TaskResponse(
            task_id=task.task_id,
            status="PENDING",
            message="Задача успешно поставлена в очередь"
        )
