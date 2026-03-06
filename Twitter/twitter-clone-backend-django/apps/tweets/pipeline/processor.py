from __future__ import annotations

from typing import Optional

import redis
from django.conf import settings
from django.utils import timezone

from apps.tweets.models import Tweet
from apps.tweets.pipeline.detector import AdHominemDetector


def _get_redis_client() -> Optional[redis.Redis]:
    if not settings.REDIS_URL:
        return None
    try:
        return redis.Redis.from_url(settings.REDIS_URL)
    except Exception:
        return None


def _is_already_processed(tweet_id: str) -> bool:
    client = _get_redis_client()
    if client is None:
        return False

    key = f"tweet-moderation:processed:{tweet_id}"
    try:
        was_set = client.set(name=key, value="1", nx=True, ex=settings.MODERATION_DEDUP_TTL_SECONDS)
        return not bool(was_set)
    except Exception:
        return False


def process_tweet_moderation_event(*, tweet_id: str, content: Optional[str] = None) -> bool:
    if _is_already_processed(tweet_id=tweet_id):
        return False

    try:
        tweet = Tweet.objects.get(id=tweet_id)
    except Tweet.DoesNotExist:
        return False

    detector = AdHominemDetector()
    detection = detector.detect(content or tweet.content)

    tweet.is_ad_hominem = detection.is_ad_hominem
    tweet.ad_hominem_score = detection.confidence
    tweet.ad_hominem_checked_at = timezone.now()
    tweet.save(update_fields=["is_ad_hominem", "ad_hominem_score", "ad_hominem_checked_at", "updated_at"])

    return True
