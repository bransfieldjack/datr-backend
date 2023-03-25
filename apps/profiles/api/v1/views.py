from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import authentication, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from ...models import Token
from ...models import User as UserModel
from .serializers import UserSerializer
from .utils import CustomizedUserPermission
from apps.memberships.models import Membership

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_model = User.objects.get(username=user)

        try:
            membership = user_model.membership
            membership = membership.active
        except Membership.DoesNotExist:
            membership = False

        token = Token.objects.get_or_create(user=user)
        return Response({
            'token': str(token[0]),
            'user_id': user.pk,
            'membership': membership,
        })


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
        operation_description="Return a user based on their token and id. ",
        manual_parameters=[
            openapi.Parameter("token", openapi.IN_QUERY,
                              description="Auth token", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Response("OK", UserSerializer)}
    )
    def retrieve(self, request, pk=None):
        try:
            instance = self.get_object()
            _user: object = Token.objects.get(key=request.auth.key).user
            user_model = User.objects.get(username=request.user)

            try:
                membership = user_model.membership
                membership = membership.active
            except Membership.DoesNotExist:
                membership = False

            serializer = UserSerializer(_user)
            reponse_data = {"user": serializer.data, "membership": membership}
            return Response(reponse_data)
        except Token.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        operation_description="Create a new user. ",
        request_body=UserSerializer,
        responses={200: openapi.Response("OK", UserSerializer)}
    )
    def create(self, request, *args, **kwargs):

        _user = request.data['username']
        if _user is not None:
            # A backend authenticated the credentials
            try:
                user = User.objects.get(
                    username=_user)
                user_token = Token.objects.get(user=user)
                return Response({"id": user.id, "token": str(user_token)})
            except User.DoesNotExist:
                user = User.objects.create(
                    username=_user, password=make_password(request.data['password']))
                user_token = Token.objects.get(user=user)
                return Response({"id": user.id, "token": str(user_token)})

        else:
            # No backend authenticated the credentials
            return Response([], status=status.HTTP_401_UNAUTHORIZED)
