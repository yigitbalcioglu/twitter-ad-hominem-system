import time

from django.core.management.base import BaseCommand

from apps.tweets.models import Tweet
from apps.tweets.pipeline.kafka import publish_tweet_created_event


class Command(BaseCommand):
    help = "Publish unchecked tweets periodically for moderation pipeline."

    def add_arguments(self, parser):
        parser.add_argument("--interval-seconds", type=int, default=60)
        parser.add_argument("--batch-size", type=int, default=100)

    def handle(self, *args, **options):
        interval_seconds = max(1, options["interval_seconds"])
        batch_size = max(1, options["batch_size"])

        self.stdout.write(self.style.SUCCESS("Moderation scheduler started."))
        self.stdout.write(f"Interval: {interval_seconds}s | Batch size: {batch_size}")

        while True:
            queryset = Tweet.objects.filter(ad_hominem_checked_at__isnull=True).order_by("created_at")[:batch_size]

            published_count = 0
            for tweet in queryset:
                if publish_tweet_created_event(tweet=tweet):
                    published_count += 1

            self.stdout.write(f"Published {published_count} events. Sleeping {interval_seconds}s...")
            time.sleep(interval_seconds)
