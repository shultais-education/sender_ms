from typing import Annotated, TypeAlias
from fastapi import Depends
from app.services.messages import MessageService


def get_message_service() -> MessageService:
    return MessageService()


MessageServiceDep: TypeAlias = Annotated[MessageService, Depends(get_message_service)]
