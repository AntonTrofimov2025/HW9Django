from rest_framework import serializers
from apps.tasks.models import Category
from .task import TaskDetailSerializer


class CategorySerializer(serializers.ModelSerializer):

    tasks = TaskDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['name', 'tasks', 'is_deleted']
        read_only_fields = ['is_deleted', 'deleted_at']

class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']
        read_only_fields = ['id', 'is_deleted', 'deleted_at']

    def create(self, validated_data):
        if Category.all_objects.filter(name=validated_data.get('name')).exists():
            raise serializers.ValidationError('This category name already exists.')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name and Category.all_objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError('This category name already exists.')
        return super().update(instance, validated_data)

