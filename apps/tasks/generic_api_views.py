from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     GenericAPIView)
from apps.tasks.models import SubTask, Task
from .serializers import (SubTaskSerializer, SubTaskCreateSerializer,
                          TaskSerializer, TaskDetailSerializer, TaskCreateSerializer)
from .paginators import SubTaskPaginator, TaskPaginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.utils import timezone
from rest_framework.response import Response
from django.db.models import Q, Count
from rest_framework import status
from apps.core.models import Statuses


class SubTaskListCreateView(ListCreateAPIView):

    queryset = SubTask.objects.select_related('task').all()
    serializer_class = SubTaskSerializer
    pagination_class = SubTaskPaginator

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['deadline', 'status']
    ordering_fields = ['created_at']
    search_fields = ['title', 'description']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubTaskCreateSerializer
        return SubTaskSerializer

class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    queryset = SubTask.objects.select_related('task').all()
    serializer_class = SubTaskSerializer


class TaskListCreateView(ListCreateAPIView):

    queryset = Task.objects.prefetch_related('categories', 'subtasks').all()
    serializer_class = TaskSerializer
    pagination_class = TaskPaginator

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskSerializer

class TaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):

    queryset = Task.objects.prefetch_related('categories', 'subtasks').all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskSerializer

class TaskStatistics(GenericAPIView):

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        tasks_aggregation = Task.objects.aggregate(total_count=Count('id'),
                                                   expired_tasks=Count('id', filter=Q(deadline__lt=now)),
        **{f'{status__.value}_count': Count('id', filter=Q(status=status__.value)) for status__ in Statuses})
        return Response({'Statistics': tasks_aggregation}, status=status.HTTP_200_OK)


