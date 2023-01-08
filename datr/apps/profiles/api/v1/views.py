from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from ...models import Token
from ...models import User as UserModel
from .serializers import UserSerializer
from .utils import CustomizedUserPermission

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """
    http_method_names = ["post", "get", "delete"]

    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [CustomizedUserPermission, ]

    @swagger_auto_schema(auto_schema=None)
    def list(self, request):
        pass

    @swagger_auto_schema(
        operation_description="Return a user based on their token. ",
        manual_parameters=[
            openapi.Parameter("token", openapi.IN_QUERY,
                              description="Auth token", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response("OK", UserSerializer)}
    )
    def retrieve(self, request, pk=None):

        print(" ")
        print("checking if this thing ifres")
        print(" ")
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        print("retrieve fires, output of serializer: ", serializer)
        print(" ")
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        _user = request.data['username']
        if _user is not None:
            # A backend authenticated the credentials
            try:
                user = User.objects.get(
                    username=_user)
                user_token = Token.objects.get(user=user)
                return Response({"token": str(user_token)})
            except User.DoesNotExist:
                user = User.objects.create(
                    username=_user, password=make_password(request.data['password']))
                user_token = Token.objects.get(user=user)
                return Response({"token": str(user_token)})

        else:
            # No backend authenticated the credentials
            return Response([], status=status.HTTP_401_UNAUTHORIZED)
