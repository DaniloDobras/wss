import os

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    KAFKA_CONSUME_TOPIC: str = os.getenv('KAFKA_CONSUME_TOPIC')
    KAFKA_PRODUCE_TOPIC: str = os.getenv('KAFKA_PRODUCE_TOPIC')


settings = Settings()
