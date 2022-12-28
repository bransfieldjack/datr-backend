from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_schema_view(
    openapi.Info(
        title="DATr API",
        default_version="v1",
        description="Description",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r"^swagger(?P<format>\.json|\.yaml)$",
            login_required(schema_view.without_ui(cache_timeout=0)), name="schema-json"),
    re_path(r"^swagger/$", schema_view.with_ui("swagger",
            cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^redoc/$", login_required(schema_view.with_ui("redoc",
            cache_timeout=0)), name="schema-redoc"),
    path("admin/", admin.site.urls),
    re_path(r"^api/v1/user/", include(("datr.apps.profiles.api.v1.urls",
            "datr.apps.profiles.api.v1.urls"), namespace="api_v1_user")),
    re_path(r"^api/v1/token/", obtain_auth_token,
            name='api_v1_token_auth'),
]
