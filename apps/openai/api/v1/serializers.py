from rest_framework import serializers


class MarketingChatSerializer(serializers.Serializer):
    company = serializers.CharField(max_length=200)
    bio_information = serializers.CharField(max_length=2000)
    keywords = serializers.CharField(max_length=500)
    tone = serializers.CharField(max_length=200)
    output_format = serializers.CharField(max_length=200)
