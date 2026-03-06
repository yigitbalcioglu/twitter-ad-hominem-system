from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel
from apps.users.models import User


class Tweet(UUIDModel, TimeStampedModel):
    author = models.ForeignKey(User, related_name="tweets", on_delete=models.CASCADE)
    content = models.CharField(max_length=280)
    reply_to = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    repost_of = models.ForeignKey(
        "self",
        related_name="reposts",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_ad_hominem = models.BooleanField(null=True, blank=True, db_index=True)
    ad_hominem_score = models.FloatField(null=True, blank=True)
    ad_hominem_checked_at = models.DateTimeField(null=True, blank=True, db_index=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:30]}"

    class Meta:
        ordering = ["-created_at"]


class TweetMedia(UUIDModel, TimeStampedModel):
    MEDIA_IMAGE = "image"
    MEDIA_VIDEO = "video"

    MEDIA_TYPES = (
        (MEDIA_IMAGE, "Image"),
        (MEDIA_VIDEO, "Video"),
    )

    tweet = models.ForeignKey(Tweet, related_name="media", on_delete=models.CASCADE)
    url = models.URLField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)


class Like(TimeStampedModel):
    user = models.ForeignKey(User, related_name="likes", on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="likes", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "tweet"], name="unique_like"),
        ]


class Retweet(TimeStampedModel):
    user = models.ForeignKey(User, related_name="retweets", on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, related_name="retweets", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "tweet"], name="unique_retweet"),
        ]

