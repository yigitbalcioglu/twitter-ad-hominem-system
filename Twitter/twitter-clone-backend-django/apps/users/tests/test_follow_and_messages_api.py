from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import Follow, User


class FollowAndMessagesApiTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            username="user1",
            password="strong-pass-123",
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com",
            username="user2",
            password="strong-pass-456",
        )
        self.client.force_authenticate(user=self.user1)

    def test_follow_toggle_flow(self):
        toggle_url = f"/api/v1/auth/follows/{self.user2.id}/toggle/"
        status_url = f"/api/v1/auth/follows/status/?user_id={self.user2.id}"

        follow_response = self.client.post(toggle_url, format="json")
        self.assertEqual(follow_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(follow_response.data["following"], True)
        self.assertTrue(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

        status_response = self.client.get(status_url)
        self.assertEqual(status_response.status_code, status.HTTP_200_OK)
        self.assertEqual(status_response.data["following"], True)

        unfollow_response = self.client.post(toggle_url, format="json")
        self.assertEqual(unfollow_response.status_code, status.HTTP_200_OK)
        self.assertEqual(unfollow_response.data["following"], False)
        self.assertFalse(Follow.objects.filter(follower=self.user1, following=self.user2).exists())

    def test_messages_require_following(self):
        message_url = f"/api/v1/auth/messages/{self.user2.id}/"

        response = self.client.post(message_url, {"text": "selam"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_messages_work_for_followed_users(self):
        Follow.objects.create(follower=self.user1, following=self.user2)
        message_url = f"/api/v1/auth/messages/{self.user2.id}/"

        send_response = self.client.post(message_url, {"text": "selam"}, format="json")
        self.assertEqual(send_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(send_response.data["text"], "selam")

        list_response = self.client.get(message_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data), 1)
        self.assertEqual(list_response.data[0]["text"], "selam")

        contacts_response = self.client.get("/api/v1/auth/messages/contacts/")
        self.assertEqual(contacts_response.status_code, status.HTTP_200_OK)
        usernames = [item["username"] for item in contacts_response.data]
        self.assertIn(self.user2.username, usernames)
