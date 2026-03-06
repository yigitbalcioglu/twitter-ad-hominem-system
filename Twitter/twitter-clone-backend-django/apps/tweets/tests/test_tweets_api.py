from rest_framework import status
from rest_framework.test import APITestCase

from apps.tweets.models import Like, Retweet, Tweet
from apps.users.models import User


class TweetApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user1@example.com",
            username="user1",
            password="strong-pass-123",
        )
        self.other_user = User.objects.create_user(
            email="user2@example.com",
            username="user2",
            password="strong-pass-456",
        )

    def authenticate(self, user, password):
        token_url = "/api/v1/auth/token/"
        response = self.client.post(
            token_url,
            {"email": user.email, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access = response.data.get("access")
        self.assertTrue(access)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_list_tweets_is_public(self):
        Tweet.objects.create(author=self.other_user, content="Hello world")

        response = self.client.get("/api/v1/tweets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_tweet_requires_auth(self):
        payload = {"content": "New tweet"}

        response = self.client.post("/api/v1/tweets/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_tweet_with_auth(self):
        self.authenticate(self.user, "strong-pass-123")

        payload = {"content": "New tweet"}
        response = self.client.post("/api/v1/tweets/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get("content"), payload["content"])
        self.assertEqual(str(response.data.get("author")), str(self.user.id))

    def test_like_and_unlike_tweet(self):
        tweet = Tweet.objects.create(author=self.other_user, content="Like me")
        self.authenticate(self.user, "strong-pass-123")

        like_response = self.client.post(f"/api/v1/tweets/{tweet.id}/like/")

        self.assertEqual(like_response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, tweet=tweet).exists())

        unlike_response = self.client.post(f"/api/v1/tweets/{tweet.id}/unlike/")

        self.assertEqual(unlike_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(user=self.user, tweet=tweet).exists())

    def test_create_retweet(self):
        tweet = Tweet.objects.create(author=self.other_user, content="Retweet me")
        self.authenticate(self.user, "strong-pass-123")

        payload = {"tweet": str(tweet.id)}
        response = self.client.post("/api/v1/retweets/", payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Retweet.objects.filter(user=self.user, tweet=tweet).exists())
