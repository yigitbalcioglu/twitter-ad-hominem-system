from unittest.mock import patch

from django.test import TestCase

from apps.tweets.models import Tweet
from apps.tweets.pipeline.detector import DetectionResult
from apps.tweets.pipeline.processor import process_tweet_moderation_event
from apps.tweets.services import create_tweet
from apps.users.models import User


class ModerationPipelineTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="moderation@example.com",
            username="moderation_user",
            password="strong-pass-123",
        )

    @patch("apps.tweets.services.publish_tweet_created_event")
    def test_create_tweet_persists_first_and_publishes_event(self, mock_publish):
        mock_publish.return_value = True

        tweet = create_tweet(author=self.user, content="test içerik")

        self.assertIsNotNone(tweet.id)
        self.assertIsNone(tweet.is_ad_hominem)
        self.assertIsNone(tweet.ad_hominem_score)
        self.assertIsNone(tweet.ad_hominem_checked_at)
        mock_publish.assert_called_once_with(tweet=tweet)

    @patch("apps.tweets.pipeline.processor.AdHominemDetector")
    @patch("apps.tweets.pipeline.processor._is_already_processed")
    def test_process_event_updates_tweet_fields(self, mock_dedup, mock_detector_cls):
        mock_dedup.return_value = False
        mock_detector = mock_detector_cls.return_value
        mock_detector.detect.return_value = DetectionResult(
            is_ad_hominem=True,
            confidence=0.91,
            source="test",
        )

        tweet = Tweet.objects.create(author=self.user, content="sen cahilsin")

        updated = process_tweet_moderation_event(tweet_id=str(tweet.id), content=tweet.content)

        self.assertTrue(updated)
        tweet.refresh_from_db()
        self.assertTrue(tweet.is_ad_hominem)
        self.assertAlmostEqual(tweet.ad_hominem_score, 0.91, places=2)
        self.assertIsNotNone(tweet.ad_hominem_checked_at)

    @patch("apps.tweets.pipeline.processor.AdHominemDetector")
    @patch("apps.tweets.pipeline.processor._is_already_processed")
    def test_process_event_skips_when_already_processed(self, mock_dedup, mock_detector_cls):
        mock_dedup.return_value = True

        tweet = Tweet.objects.create(author=self.user, content="normal tweet")

        updated = process_tweet_moderation_event(tweet_id=str(tweet.id), content=tweet.content)

        self.assertFalse(updated)
        mock_detector_cls.assert_not_called()

    def test_heuristic_detector_flags_attack_keywords(self):
        from apps.tweets.pipeline.detector import AdHominemDetector

        detector = AdHominemDetector()
        result = detector._detect_with_heuristic("Sen tam bir cahilsin.")

        self.assertTrue(result.is_ad_hominem)
        self.assertGreater(result.confidence, 0.3)

    @patch("apps.tweets.pipeline.detector.requests.post")
    def test_remote_detector_handles_invalid_confidence_payload(self, mock_post):
        from apps.tweets.pipeline.detector import AdHominemDetector

        mock_response = mock_post.return_value
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "is_ad_hominem": True,
            "confidence": None,
        }

        detector = AdHominemDetector()
        result = detector._detect_with_remote_model("örnek metin")

        self.assertIsNotNone(result)
        self.assertTrue(result.is_ad_hominem)
        self.assertEqual(result.confidence, 0.0)
