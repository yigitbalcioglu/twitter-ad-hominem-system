import logging

from apps.tweets.models import Like, Tweet
from apps.tweets.pipeline.kafka import publish_tweet_created_event
from apps.users.models import User


logger = logging.getLogger(__name__)


def create_tweet(*, author: User, content: str, reply_to=None, repost_of=None) -> Tweet:
    tweet = Tweet.objects.create(
        author=author,
        content=content,
        reply_to=reply_to,
        repost_of=repost_of,
        is_ad_hominem=None,
        ad_hominem_score=None,
        ad_hominem_checked_at=None,
    )

    published = publish_tweet_created_event(tweet=tweet)
    if not published:
        logger.warning("Tweet moderation event could not be published for tweet %s", tweet.id)

    return tweet


def like_tweet(*, user: User, tweet: Tweet) -> Like:
    like, _created = Like.objects.get_or_create(user=user, tweet=tweet)
    return like


def unlike_tweet(*, user: User, tweet: Tweet) -> None:
    Like.objects.filter(user=user, tweet=tweet).delete()
