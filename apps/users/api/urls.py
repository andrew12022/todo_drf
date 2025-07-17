from rest_framework import routers

from apps.users.api.views import UserViewSet

router_v1 = routers.DefaultRouter()


router_v1.register(
    'users',
    UserViewSet,
    basename='users',
)

urlpatterns = router_v1.urls
