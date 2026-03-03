from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class MessageRequest(BaseModel):
    subject: str = Field(min_length=1, max_length=100, description="Тема сообщения")
    text: str = Field(min_length=1, max_length=1000, description="Текст сообщения")
    to: EmailStr

    delay: Optional[int] = Field(0, description="Задержка выполнения в секундах")


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str
