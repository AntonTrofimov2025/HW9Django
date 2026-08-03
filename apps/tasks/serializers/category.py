from rest_framework import serializers
from apps.tasks.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['name']

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data.get('name')).exists():
            raise serializers.ValidationError('This category name already exists.')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        if name:
            if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
                raise serializers.ValidationError('This category name already exists.')
        return super().update(instance, validated_data)

