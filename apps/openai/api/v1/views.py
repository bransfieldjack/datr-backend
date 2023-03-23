from django.http import Http404
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .serializers import MarketingChatSerializer
from apps.profiles.api.v1.utils import CustomizedUserPermission


class MarketingGptViewset(ViewSet):
    """
    Interface with gpt
    """
    http_method_names = ["post", "get", "delete"]
    serializer_class = MarketingChatSerializer
    permission_classes = [CustomizedUserPermission, ]

    @swagger_auto_schema(
        operation_description="Return a response from openai marketing chat. ",
        manual_parameters=[
            openapi.Parameter("token", openapi.IN_QUERY,
                              description="Auth token", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response("OK", MarketingChatSerializer)}
    )
    def create(self, request, format=None):
        serializer = MarketingChatSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
