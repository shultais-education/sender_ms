from app.schemas.message import TaskResponse


class MessageService:

    @staticmethod
    async def send_message(message: str, delay: int = 0) -> TaskResponse:
        return TaskResponse(
            task_id="1",
            status="статус",
            message=message
        )
