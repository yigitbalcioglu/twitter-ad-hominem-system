from django.core.management.base import BaseCommand

from apps.tweets.pipeline.kafka import consume_messages
from apps.tweets.pipeline.processor import process_tweet_moderation_event


class Command(BaseCommand):
    help = "Consume tweet moderation events from Kafka and update tweet ad hominem flags."

    def add_arguments(self, parser):
        parser.add_argument("--max-messages", type=int, default=0)
        parser.add_argument("--group-id", type=str, default=None)
        parser.add_argument("--from-beginning", action="store_true")

    def handle(self, *args, **options):
        max_messages = options["max_messages"]
        group_id = options["group_id"]
        auto_offset_reset = "earliest" if options["from_beginning"] else "latest"

        processed_count = 0
        for payload in consume_messages(group_id=group_id, auto_offset_reset=auto_offset_reset):
            tweet_id = str(payload.get("tweet_id", "")).strip()
            if not tweet_id:
                continue

            content = payload.get("content")
            updated = process_tweet_moderation_event(tweet_id=tweet_id, content=content)
            if updated:
                processed_count += 1
                self.stdout.write(self.style.SUCCESS(f"Processed tweet {tweet_id}"))

            if max_messages and processed_count >= max_messages:
                break

        self.stdout.write(self.style.SUCCESS(f"Finished. Processed: {processed_count}"))
