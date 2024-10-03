from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .serializers import TweetSerializer
from .models import Tweet


@api_view(["GET"])
def tweets(request):
    if request.method == "GET":
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(all_tweets, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def tweet(request, pk):
    try:
        tweet = Tweet.objects.get(pk=pk)
    except Tweet.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)
