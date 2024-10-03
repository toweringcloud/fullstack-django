from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer
from tweets.serializers import TweetSerializer


@api_view(["GET"])
def users(request):
    if request.method == "GET":
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFound

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(["GET"])
def user_tweets(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        serializer = TweetSerializer(user.tweets, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        raise NotFound
