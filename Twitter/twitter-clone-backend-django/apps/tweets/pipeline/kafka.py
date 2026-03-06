from __future__ import annotations

import json
import logging
from typing import Dict, Iterable, Optional

from django.conf import settings

logger = logging.getLogger(__name__)


try:
    from kafka import KafkaConsumer, KafkaProducer
except Exception:  # pragma: no cover
    KafkaConsumer = None
    KafkaProducer = None


def _kafka_enabled() -> bool:
    return bool(settings.KAFKA_ENABLED and KafkaProducer is not None and KafkaConsumer is not None)


def _bootstrap_servers() -> list[str]:
    return [server.strip() for server in settings.KAFKA_BOOTSTRAP_SERVERS.split(",") if server.strip()]


def get_kafka_producer() -> Optional[object]:
    if not _kafka_enabled():
        return None
    return KafkaProducer(
        bootstrap_servers=_bootstrap_servers(),
        value_serializer=lambda value: json.dumps(value).encode("utf-8"),
    )


def publish_tweet_created_event(*, tweet) -> bool:
    producer = get_kafka_producer()
    if producer is None:
        return False

    payload = {
        "tweet_id": str(tweet.id),
        "content": tweet.content,
        "created_at": tweet.created_at.isoformat(),
    }

    try:
        producer.send(settings.KAFKA_TWEET_TOPIC, payload)
        producer.flush(timeout=10)
        return True
    except Exception as exc:  # pragma: no cover
        logger.warning("Failed to publish moderation event for tweet %s: %s", tweet.id, exc)
        return False


def get_kafka_consumer(*, group_id: Optional[str] = None, auto_offset_reset: str = "latest") -> Optional[object]:
    if not _kafka_enabled():
        return None

    consumer_group = group_id or settings.KAFKA_TWEET_GROUP_ID
    return KafkaConsumer(
        settings.KAFKA_TWEET_TOPIC,
        bootstrap_servers=_bootstrap_servers(),
        group_id=consumer_group,
        auto_offset_reset=auto_offset_reset,
        value_deserializer=lambda value: json.loads(value.decode("utf-8")),
        enable_auto_commit=True,
    )


def consume_messages(*, group_id: Optional[str] = None, auto_offset_reset: str = "latest") -> Iterable[Dict[str, object]]:
    consumer = get_kafka_consumer(group_id=group_id, auto_offset_reset=auto_offset_reset)
    if consumer is None:
        return []

    for message in consumer:
        if isinstance(message.value, dict):
            yield message.value
