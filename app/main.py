import threading
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.kafka_worker import start_kafka_consumer
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):

    print("WSS lifespan started.")
    kafka_thread = threading.Thread(target=start_kafka_consumer, daemon=True)
    kafka_thread.start()
    yield

app = FastAPI(lifespan=lifespan)


# Allow requests from Angular app
origins = [
    "http://localhost:4200",  # Angular dev server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # origins allowed to access
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods
    allow_headers=["*"],              # allow all headers
)

app.include_router(router)