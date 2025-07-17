from rest_framework import routers

from apps.tasks.api.views import CategoryViewSet, TagViewSet, TaskViewSet

router_v1 = routers.DefaultRouter()


router_v1.register(
    'tasks',
    TaskViewSet,
    basename='tasks',
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories',
)
router_v1.register(
    'tags',
    TagViewSet,
    basename='tags',
)

urlpatterns = router_v1.urls
