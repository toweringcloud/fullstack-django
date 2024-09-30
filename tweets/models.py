from django.db import models
from common.models import Common


class Tweet(Common):
    """Tweet Model Definition"""

    payload = models.CharField(
        max_length=180,
        default="",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.payload

    def likes_count(self):
        return self.likes.count()


class Like(Common):
    """Like Model Definition"""

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    tweet = models.ForeignKey(
        "tweets.Tweet",
        on_delete=models.CASCADE,
        related_name="likes",
    )

    def __str__(self):
        return self.tweet.payload
