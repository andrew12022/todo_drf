from rest_framework import serializers

from apps.tasks.models import Category, Tag, Task


class TaskSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Task
        exclude = (
            'slug',
        )


class CategorySerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Category
        exclude = (
            'slug',
        )


class TagSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        model = Tag
        exclude = (
            'slug',
        )
