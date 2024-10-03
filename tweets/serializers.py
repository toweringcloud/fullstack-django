from rest_framework import serializers
from .models import Tweet


class TweetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    payload = serializers.CharField(
        max_length=180,
        required=True,
    )
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.CharField(read_only=True)

    def create(self, validated_data):
        return Tweet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.payload = validated_data.get("payload", instance.payload)
        instance.save()
        return instance
