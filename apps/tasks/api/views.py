from rest_framework import viewsets

from apps.tasks.api.serializers import (CategorySerializer, TagSerializer,
                                        TaskSerializer)
from apps.tasks.models import Category, Tag, Task


class TaskViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    """."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
