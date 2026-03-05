from fastapi import APIRouter, HTTPException
from fastapi import status
from typing import Union, List

from app.schemas.message import MessageRequest, TaskResponse
from app.api.dependencies.messages import MessageServiceDep
from app.api.dependencies.security import KeyHeaderDep


messages_router = APIRouter(prefix="/messages", tags=["messages"])


@messages_router.post("", response_model=List[TaskResponse], summary="Отправка сообщения", status_code=status.HTTP_202_ACCEPTED)
async def send_message(
        messages: Union[MessageRequest, List[MessageRequest]],
        message_service: MessageServiceDep,
        api_key: KeyHeaderDep
):
    if api_key not in ('abc', 'ABC'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный ключ")

    if isinstance(messages, MessageRequest):
        messages = [messages]

    # results = []
    #
    # for message in messages:
    #     result = await message_service.send_message(
    #         subject=message.subject,
    #         text=message.text,
    #         to=message.to,
    #         delay=message.delay
    #     )
    #     results.append(result)
    #
    # return results

    # tasks = []
    # for message in messages:
    #     tasks.append(asyncio.create_task(message_service.send_message(
    #         subject=message.subject,
    #         text=message.text,
    #         to=message.to,
    #         delay=message.delay
    #     )))

    # return await asyncio.gather(*tasks)

    results = [await message_service.send_messages(messages=[m.model_dump() for m in messages])]
    return results

