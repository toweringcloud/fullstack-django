from django.contrib.auth import authenticate, login, logout
from rest_framework.exceptions import (
    NotFound,
    ParseError,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from tweets.serializers import TweetSerializer
from .models import User
from .serializers import PrivateUserSerializer, TinyUserSerializer


class Users(APIView):
    # GET /api/v1/users: See all users
    def get(self, request):
        all_users = User.objects.all()
        serializer = TinyUserSerializer(all_users, many=True)
        return Response(serializer.data)

    # POST /api/v1/users: Create a user account with password
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = PrivateUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=HTTP_400_BAD_REQUEST,
            )


class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound

    # GET /api/v1/users/<int:pk>: See user profile
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)


class UserTweets(APIView):
    # GET /api/v1/users/<int:pk>/tweets: See tweets by a user
    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = TweetSerializer(user.tweets, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise NotFound


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    # PUT /api/v1/users/password: Change password of logged in user
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            raise ParseError


class LogIn(APIView):
    # POST /api/v1/users/login: Log user in
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError

        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok": "Welcome!"})
        else:
            return Response(
                {"error": "wrong password"},
                status=HTTP_400_BAD_REQUEST,
            )


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    # POST /api/v1/users/logout: Log user out
    def post(self, request):
        logout(request)
        return Response({"ok": "bye!"})
