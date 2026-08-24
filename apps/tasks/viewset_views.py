from rest_framework.response import Response
from rest_framework import status
from apps.tasks.models import Category
from rest_framework import viewsets
from apps.tasks.serializers import CategorySerializer, CategoryCreateSerializer
from django.db import transaction
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.filters import OrderingFilter


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.prefetch_related('tasks', 'tasks__subtasks')
    serializer_class = CategorySerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['name']
    ordering = ('name',)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CategoryCreateSerializer
        return CategorySerializer

    @action(detail=False, methods=['get'], url_name='count', url_path='count')
    def count_tasks(self, *args, **kwargs):
        all_tasks = Category.objects.annotate(tasks_count=Count('tasks__id')).values('name', 'tasks_count')
        return Response(list(all_tasks), status=status.HTTP_200_OK)

