from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from tweets.serializers import TweetSerializer
from .models import User
from .serializers import PrivateUserSerializer, TinyUserSerializer


class Users(APIView):
    # GET /api/v1/users
    def get(self, request):
        all_users = User.objects.all()
        serializer = TinyUserSerializer(all_users, many=True)
        return Response(serializer.data)


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    # GET /api/v1/users/<int:pk>
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class UserTweets(APIView):
    # GET /api/v1/users/<int:pk>/tweets
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = TweetSerializer(user.tweets, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise NotFound
