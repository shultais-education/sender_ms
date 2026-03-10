from fastapi import FastAPI
from app.api.endpoints.messages import messages_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan, title="API сообщений", description="Микросервис для отправки сообщений", root_path="/api")
app.include_router(messages_router)
