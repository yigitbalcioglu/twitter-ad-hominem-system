from django.core.management.base import BaseCommand

from apps.tweets.models import Tweet
from apps.tweets.pipeline.kafka import publish_tweet_created_event


class Command(BaseCommand):
    help = "Publish unchecked tweets to Kafka moderation topic."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        limit = options["limit"]
        queryset = Tweet.objects.filter(ad_hominem_checked_at__isnull=True).order_by("created_at")[:limit]

        published_count = 0
        for tweet in queryset:
            if publish_tweet_created_event(tweet=tweet):
                published_count += 1

        self.stdout.write(self.style.SUCCESS(f"Published {published_count} tweet events"))
