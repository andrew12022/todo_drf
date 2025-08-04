from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import SAFE_METHODS

from apps.tasks.api.serializers import (CategorySerializer, TagSerializer,
                                        TaskCreateSerializer,
                                        TaskReadSerializer)
from apps.tasks.models import Category, Tag, Task


class OwnerViewSet(viewsets.ModelViewSet):
    """."""

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class TaskViewSet(OwnerViewSet):
    """."""

    queryset = Task.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = (
        'category__title',
        'tags__title',
        'is_done',
        'priority',
    )
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title',
        'deadline',
    )
    ordering = (
        '-id',
    )

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return TaskReadSerializer
        return TaskCreateSerializer


class CategoryViewSet(OwnerViewSet):
    """."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = (
        'title',
        'slug',
        'owner',
    )
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title',
    )
    ordering = (
        '-id',
    )


class TagViewSet(OwnerViewSet):
    """."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    filterset_fields = (
        'title',
        'slug',
        'owner',
    )
    search_fields = (
        'title',
    )
    ordering_fields = (
        'title',
    )
    ordering = (
        '-id',
    )
