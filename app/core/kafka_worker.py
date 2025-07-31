from kafka import KafkaConsumer, KafkaProducer
import json
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.models import Bucket, Position


producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)


def process_kafka():
    print("🚀 Starting Kafka consumer...")

    consumer = KafkaConsumer(
        settings.KAFKA_CONSUME_TOPIC,
        bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
        group_id="wss-consumer",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )

    db = SessionLocal()

    try:
        for message in consumer:
            data = message.value
            print(f"Consumed message: {data}")

            order_type = data.get("order_type")
            order_id = data.get("order_id")
            actions = data.get("actions", [])

            for action in actions:
                bucket_id = action.get("bucket_id")
                src_pos = action.get("source_position")
                tgt_pos = action.get("target_position")

                status = "not_approved"
                assigned_position = None

                if order_type == "loading":
                    # Create new bucket
                    bucket = Bucket()
                    db.add(bucket)
                    db.flush()  # to get bucket.id

                    free_pos = db.query(Position).filter(
                        ~Position.id.in_(
                            db.query(Bucket.position_id).filter(
                                Bucket.position_id.isnot(None))
                        )
                    ).first()

                    if free_pos:
                        bucket.position_id = free_pos.id
                        assigned_position = free_pos
                        status = "approved"
                    else:
                        status = "not_approved"

                elif order_type in {"unloading", "place_changing"}:
                    if not bucket_id:
                        print("Missing bucket_id in action")
                        continue

                    bucket = db.query(Bucket).filter(Bucket.id == bucket_id).first()
                    if not bucket:
                        print(f"Bucket {bucket_id} not found")
                        continue

                    if tgt_pos:
                        tgt_position = db.query(Position).filter(
                            Position.x == tgt_pos["x"],
                            Position.y == tgt_pos["y"],
                            Position.z == tgt_pos["z"]
                        ).first()

                        if tgt_position and tgt_position.bucket is None:
                            assigned_position = tgt_position
                            status = "approved"
                        else:
                            status = "not_approved"
                    else:
                        print("Missing target_position in action")

                # Send response
                response = {
                    "orderId": order_id,
                    "bucketId": bucket.id if order_type == "loading" else bucket_id,
                    "position": {
                        "x": assigned_position.x if assigned_position else None,
                        "y": assigned_position.y if assigned_position else None,
                        "z": assigned_position.z if assigned_position else None,
                    },
                    "status": status,
                    "source": "WSS"
                }

                producer.send("order.processed.plc", response)
                print(f"📤 Sent to order.processed.plc: {response}")

            db.commit()
            producer.flush()

    finally:
        db.close()


def start_kafka_consumer():
    """Starts Kafka consumer in a blocking loop (runs inside a background thread)."""
    process_kafka()
