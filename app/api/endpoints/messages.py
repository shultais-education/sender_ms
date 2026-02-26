from fastapi import APIRouter
from fastapi import status

from app.schemas.message import MessageRequest, TaskResponse
from app.api.dependencies.messages import MessageServiceDep

messages_router = APIRouter(prefix="/messages", tags=["messages"])


@messages_router.post("", response_model=TaskResponse, summary="Отправка сообщения", status_code=status.HTTP_202_ACCEPTED)
async def send_message(message: MessageRequest, message_service: MessageServiceDep):
    task = await message_service.send_message(message=message.text, delay=message.delay)

    print(message)
    print(task)

    return TaskResponse(
        task_id=task.task_id,
        status="PENDING",
        message="Задача успешно поставлена в очередь"
    )
