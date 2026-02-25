from pydantic_settings import BaseSettings
from pydantic import AmqpDsn, RedisDsn, Field
from enum import Enum


class BrokerType(str, Enum):
    RABBITMQ = "rabbitmq"
    REDIS = "redis"


class Settings(BaseSettings):
    # RabbitMQ
    RABBIT_USERNAME: str
    RABBIT_PASSWORD: str
    RABBIT_HOST: str = "localhost"
    RABBIT_PORT: int = 5672
    RABBIT_PATH: str

    # Redis Broker
    REDIS_USERNAME: str = "default"
    REDIS_PASSWORD: str = ""
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"

    # Redis Results
    REDIS_RESULTS_DB: str = "1"

    # Celery
    CELERY_TIMEZONE: str = "UTC"
    CELERY_TASK_TIME_LIMIT: int = 30 * 60
    CELERY_TASK_SOFT_TIME_LIMIT: int = 25 * 60

    # SMTP
    EMAIL_HOST: str = "localhost"
    EMAIL_PORT: int = 1025

    # Выбор брокера
    BROKER_TYPE: BrokerType = Field(
        default=BrokerType.REDIS,
        description="Тип брокера сообщений: rabbitmq или redis"
    )

    class Config:
        env_file = ".env"

    @property
    def rabbitmq_url(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.RABBIT_USERNAME,
            password=self.RABBIT_PASSWORD,
            host=self.RABBIT_HOST,
            port=self.RABBIT_PORT,
            path=self.RABBIT_PATH
        )

    @property
    def redis_url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USERNAME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_DB
        )

    @property
    def redis_results_url(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            username=self.REDIS_USERNAME,
            password=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_RESULTS_DB
        )

    @property
    def celery_broker_url(self) -> str:
        if self.BROKER_TYPE == BrokerType.RABBITMQ:
            return str(self.rabbitmq_url)
        elif self.BROKER_TYPE == BrokerType.REDIS:
            return str(self.redis_url)
        else:
            raise ValueError(f"Неподдерживаемый тип брокера: {self.BROKER_TYPE}")

    @property
    def celery_results_backend(self) -> str:
        # Пока используем Redis для результатов (даже если брокер RabbitMQ)
        return str(self.redis_results_url)


settings = Settings()
