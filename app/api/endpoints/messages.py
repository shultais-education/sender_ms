from fastapi import APIRouter
from fastapi import status
from typing import Union, List

from app.schemas.message import MessageRequest, TaskResponse
from app.api.dependencies.messages import MessageServiceDep


messages_router = APIRouter(prefix="/messages", tags=["messages"])


@messages_router.post("", response_model=List[TaskResponse], summary="Отправка сообщения", status_code=status.HTTP_202_ACCEPTED)
async def send_message(
        messages: Union[MessageRequest, List[MessageRequest]],
        message_service: MessageServiceDep
):

    if isinstance(messages, MessageRequest):
        messages = [messages]

    results = []

    for message in messages:
        result = await message_service.send_message(
            subject=message.subject,
            text=message.text,
            to=message.to,
            delay=message.delay
        )
        results.append(result)

    return results

