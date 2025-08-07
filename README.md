# Warehouse State Service (WSS)

The **Warehouse State Service (WSS)** is a microservice responsible for handling warehouse state updates based on incoming order actions. It consumes messages from a Kafka topic (`orders.new`) produced by the **Office Integration Service (OIS)**, processes bucket and position updates in the PostgreSQL database, and publishes results to the `order.processed.plc` Kafka topic.

---

## 📦 Functionality

- Consumes Kafka messages from `orders.new`.
- Supports three order types:
  - `loading`: Creates a new bucket and assigns it to a free position.
  - `unloading`: Validates and updates the target position of an existing bucket.
  - `place_changing`: Changes the position of a given bucket.
- Produces responses to the `order.processed.plc` topic, including approval status and assigned positions.

---

## 🛠️ Project Structure

```
.
├── alembic/               # DB migrations
├── app/
│   ├── api/               # Reserved for API routes (currently unused)
│   ├── core/
│   │   ├── config.py      # App settings via environment
│   │   └── kafka_worker.py # Kafka consumer and producer logic
│   └── db/
│       ├── database.py    # DB connection/session setup
│       └── models.py      # SQLAlchemy models: Bucket, Position
├── main.py                # Entry point for starting Kafka consumer
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Local dev orchestration with DB + Kafka net
├── .env.template          # Example environment variables
└── README.md              # You are here
```

---

## Environment Variables

Create a `.env` file based on `.env.template`. Required variables include:

```
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=wss
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_CONSUME_TOPIC=orders.new
```

---

## Running the Service

```bash
docker-compose up --build
```

- The service runs on port `8002`.
- It connects to the external Docker network `shared-kafka-net` for Kafka integration.

---

## Kafka Topics

- **Consumes from**: `orders.new`
- **Produces to**: `order.processed.plc`

Example of a consumed message:

```json
{
  "order_id": "1234",
  "order_type": "loading",
  "actions": [
    {
      "bucket_id": null,
      "source_position": null,
      "target_position": null
    }
  ]
}
```

Example of a produced message:

```json
{
  "orderId": "1234",
  "bucketId": 5,
  "position": {
    "x": 1,
    "y": 2,
    "z": 3
  },
  "status": "approved",
  "source": "WSS"
}
```

---

## Database

- PostgreSQL 15
- Exposed on host port `5433`
- Alembic is used for schema migrations

## Run Alembic Migrations

### Initialize the database:

```bash
docker exec -it wss-service alembic upgrade head
```

### Create a new migration:

```bash
docker exec -it wss-service alembic revision --autogenerate -m "table added"
```

---