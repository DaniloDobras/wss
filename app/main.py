import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.kafka_worker import start_kafka_consumer


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("WSS lifespan started.")
    kafka_thread = threading.Thread(target=start_kafka_consumer, daemon=True)
    kafka_thread.start()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)