from rest_framework import status
from rest_framework.test import APITestCase

from apps.tweets.models import Tweet
from apps.users.models import User


class MultiUserRegisterAndTweetFlowTests(APITestCase):
    def register_user(self, *, email: str, username: str, password: str) -> dict:
        response = self.client.post(
            "/api/v1/auth/register/",
            {
                "email": email,
                "username": username,
                "password": password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def login_and_set_auth(self, *, email: str, password: str) -> str:
        response = self.client.post(
            "/api/v1/auth/token/",
            {
                "email": email,
                "password": password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        access = response.data.get("access")
        self.assertTrue(access)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        return access

    def create_tweet(self, *, content: str) -> dict:
        response = self.client.post(
            "/api/v1/tweets/",
            {"content": content},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def test_multiple_registered_users_can_create_tweets(self):
        users = [
            {
                "email": "ali@example.com",
                "username": "ali",
                "password": "strong-pass-123",
                "content": "Ali'den ilk tweet",
            },
            {
                "email": "ayse@example.com",
                "username": "ayse",
                "password": "strong-pass-456",
                "content": "Ayse'den ilk tweet",
            },
            {
                "email": "mehmet@example.com",
                "username": "mehmet",
                "password": "strong-pass-789",
                "content": "Mehmet'ten ilk tweet",
            },
        ]

        created_tweet_ids = []

        for user_data in users:
            self.register_user(
                email=user_data["email"],
                username=user_data["username"],
                password=user_data["password"],
            )

            self.assertTrue(User.objects.filter(email=user_data["email"]).exists())

            self.login_and_set_auth(
                email=user_data["email"],
                password=user_data["password"],
            )

            created_tweet = self.create_tweet(content=user_data["content"])
            created_tweet_ids.append(created_tweet["id"])

            user = User.objects.get(email=user_data["email"])
            self.assertEqual(str(created_tweet["author"]), str(user.id))

            self.client.credentials()

        self.assertEqual(Tweet.objects.count(), 3)

        list_response = self.client.get("/api/v1/tweets/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertIn("results", list_response.data)

        listed_tweet_ids = {item["id"] for item in list_response.data["results"]}
        self.assertTrue(set(created_tweet_ids).issubset(listed_tweet_ids))
