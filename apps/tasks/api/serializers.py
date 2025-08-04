from django.utils.text import slugify

from rest_framework import serializers

from apps.tasks.models import Category, Tag, Task


class AutoSlugOwnerSerializer(serializers.ModelSerializer):
    """."""

    owner = serializers.StringRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['title'])
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])
        return super().update(instance, validated_data)


class TaskReadSerializer(serializers.ModelSerializer):
    """."""

    priority = serializers.CharField(
        source='get_priority_display',
        read_only=True,
    )
    category = serializers.StringRelatedField(
        read_only=True,
    )
    tags = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    owner = serializers.StringRelatedField(
        read_only=True,
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'is_done',
            'deadline',
            'priority',
            'created_at',
            'updated_at',
            'category',
            'tags',
            'owner',
        )


class TaskCreateSerializer(AutoSlugOwnerSerializer):
    """."""

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'slug',
            'description',
            'is_done',
            'deadline',
            'priority',
            'created_at',
            'updated_at',
            'category',
            'tags',
            'owner',
        )

    def validate_category(self, category):
        if category.owner != self.context['request'].user:
            raise serializers.ValidationError(
                f'Категория "{category.title}" вам не принадлежит!'
            )
        return category

    def validate_tags(self, tags):
        for tag in tags:
            if tag.owner != self.context['request'].user:
                raise serializers.ValidationError(
                    f'Тег "{tag.title}" вам не принадлежит!'
                )
        return tags

    def to_representation(self, instance):
        return TaskReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            },
        ).data


class CategorySerializer(AutoSlugOwnerSerializer):
    """."""

    class Meta:
        model = Category
        fields = (
            'id',
            'title',
            'slug',
            'owner',
        )


class TagSerializer(AutoSlugOwnerSerializer):
    """."""

    class Meta:
        model = Tag
        fields = (
            'id',
            'title',
            'slug',
            'owner',
        )
