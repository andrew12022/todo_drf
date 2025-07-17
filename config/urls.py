from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from apps.tasks.api.urls import router_v1 as tasks_router_v1
from apps.users.api.urls import router_v1 as users_router_v1

main_router_v1 = DefaultRouter()
main_router_v1.registry.extend(tasks_router_v1.registry)
main_router_v1.registry.extend(users_router_v1.registry)

urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        'api/',
        include(main_router_v1.urls),
    ),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='docs',
    ),
]
