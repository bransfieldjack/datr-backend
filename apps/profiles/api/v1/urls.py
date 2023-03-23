from .views import UserViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'', UserViewSet, basename='/api/v1/user')
urlpatterns = router.urls
