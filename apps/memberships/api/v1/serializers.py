# serializers.py
from rest_framework import serializers


class SubscriptionSerializer(serializers.Serializer):
    plan = serializers.CharField()
    success_url = serializers.CharField()
    cancel_url = serializers.CharField()
