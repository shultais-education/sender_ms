from pydantic import BaseModel, Field
from typing import Optional


class MessageRequest(BaseModel):
    text: str = Field(min_length=1, max_length=1000, description="Текст сообщения")
    delay: Optional[int] = Field(0, description="Задержка выполнения в секундах")


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
