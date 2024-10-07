from rest_framework.exceptions import (
    NotAuthenticated,
    NotFound,
    PermissionDenied,
)
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.views import APIView

from .models import Tweet
from .serializers import TweetSerializer


class Tweets(APIView):
    # GET /api/v1/tweets: See all tweets
    def get(self, request):
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(all_tweets, many=True)
        return Response(serializer.data)

    # POST /api/v1/tweets: Create a tweet
    def post(self, request):
        if request.user.is_authenticated:
            serializer = TweetSerializer(data=request.data)
            if serializer.is_valid():
                new_tweet = serializer.save(user=request.user)
                return Response(
                    TweetSerializer(new_tweet).data,
                )
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST,
                )

        else:
            raise NotAuthenticated


class TweetDetail(APIView):
    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound

    # GET /api/v1/tweets/<int:pk>: See a tweet
    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)

    # PUT /api/v1/tweets/<int:pk>: Edit a tweet
    def put(self, request, pk):
        tweet = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if tweet.user != request.user:
            raise PermissionDenied

        serializer = TweetSerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(
                TweetSerializer(updated_tweet).data,
            )
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )

    # DELETE /api/v1/tweets/<int:pk>: Delete a tweet
    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if tweet.user != request.user:
            raise PermissionDenied

        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)
