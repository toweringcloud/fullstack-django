from rest_framework.test import APITestCase

from users.models import User
from .models import Tweet


class TestTweets(APITestCase):

    PAYLOAD = "tweet payload"
    PAYLOAD_NEW = "tweet payload new"
    URL = "/api/v1/tweets/"

    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("1234")
        user.save()
        self.user = user

        Tweet.objects.create(
            payload=self.PAYLOAD,
            user=self.user,
        )

    def test_get_tweets(self):
        response = self.client.get(self.URL)
        data = response.json()
        print(data)

        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )
        self.assertIsInstance(
            data,
            list,
            "response type isn't list",
        )
        self.assertEqual(
            len(data),
            1,
            "data length isn't 1",
        )
        self.assertEqual(
            data[0]["payload"],
            self.PAYLOAD,
            f"payload value isn't {self.PAYLOAD}",
        )

    def test_post_tweets(self):
        self.client.force_login(
            self.user,
        )

        response = self.client.post(
            self.URL,
            data={
                "payload": self.PAYLOAD_NEW,
                "user": self.user,
            },
        )
        data = response.json()
        print(data)

        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD_NEW,
            f"payload value isn't {self.PAYLOAD_NEW}",
        )


class TestTweet(APITestCase):

    PAYLOAD = "tweet payload"
    PAYLOAD_UPDATE = "tweet payload update"
    URL = "/api/v1/tweets/1"

    def setUp(self):
        user = User.objects.create(
            username="test",
        )
        user.set_password("1234")
        user.save()
        self.user = user

        Tweet.objects.create(
            payload=self.PAYLOAD,
            user=self.user,
        )

    def test_get_tweet(self):
        response = self.client.get(
            self.URL,
            HTTP_ACCEPT="application/json",
        )
        data = response.json()
        print(data)

        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD,
            f"payload value isn't {self.PAYLOAD}",
        )

    def test_put_tweet(self):
        self.client.force_login(
            self.user,
        )

        response = self.client.put(
            self.URL,
            data={
                "payload": self.PAYLOAD_UPDATE,
                "user": self.user,
            },
        )
        data = response.json()
        print(data)

        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200.",
        )
        self.assertEqual(
            data["payload"],
            self.PAYLOAD_UPDATE,
            f"payload value isn't {self.PAYLOAD_UPDATE}",
        )

    def test_delete_tweet(self):
        self.client.force_login(
            self.user,
        )

        response = self.client.delete(
            self.URL,
        )
        print(response)

        self.assertEqual(
            response.status_code,
            204,
            "status code isn't 204.",
        )
