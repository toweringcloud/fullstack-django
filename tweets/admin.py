import operator
from django.contrib import admin
from django.db.models import Q
from functools import reduce

from .models import Tweet, Like


# Make a CUSTOM filter for Tweets that contain and don't contain the words Elon Musk
class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"

    def lookups(self, request, model_admin):
        return [
            ("in", "Include Elon Musk"),
            ("ex", "Exclude Elon Musk"),
        ]

    def queryset(self, request, tweets):
        word = self.value()
        words_filter = ["elon", "musk", "elon musk"]

        if word == "in":
            return tweets.filter(
                reduce(operator.and_, (Q(payload__contains=x) for x in words_filter))
            )
        elif word == "ex":
            return tweets.exclude(
                reduce(operator.and_, (Q(payload__contains=x) for x in words_filter))
            )
        else:
            return tweets


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payload",
        "created_at",
        "updated_at",
        "likes_count",
    )

    list_filter = (
        WordFilter,
        "created_at",
        "updated_at",
    )

    search_fields = (
        "payload",
        "user__username",
    )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tweet",
        "user",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "id",
        "created_at",
        "updated_at",
    )

    search_fields = ("user__username",)
