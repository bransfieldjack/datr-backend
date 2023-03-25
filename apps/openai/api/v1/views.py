from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import MarketingChatSerializer


class MarketingGptViewset(ViewSet):
    """
    Interface with gpt
    """
    http_method_names = ["post", "get", "delete"]
    serializer_class = MarketingChatSerializer
    authentication_classes = [authentication.TokenAuthentication]

    @swagger_auto_schema(
        operation_description="Return a response from openai marketing chat. ",
        manual_parameters=[
            openapi.Parameter("token", openapi.IN_QUERY,
                              description="Auth token", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response("OK", MarketingChatSerializer)},
        request_body=MarketingChatSerializer
    )
    def create(self, request, format=None):
        serializer = MarketingChatSerializer(data=request.data)
        if serializer.is_valid():
            from .services.openai_marketing_chat import chat_with_gpt
            try:
                response = chat_with_gpt(serializer.data)

                print("response from openai:", response)
                print(" ")
                print(" ")
                return Response({"response", response}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error", str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
