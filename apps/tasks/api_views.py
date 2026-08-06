from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from apps.tasks.models import SubTask
from .serializers import SubTaskSerializer, SubTaskCreateSerializer
from .paginators import SubTaskPaginator
from apps.core.models import Statuses


class SubTaskListCreateView(APIView):

    ALLOWED_SORT_FIELDS = ['created_at', 'deadline']

    def get(self, request):
        subtasks = SubTask.objects.select_related('task').all()
        statuses = {status_.label: status_.value for status_ in Statuses}

        filter_ = {}
        if task := request.query_params.get('task'):
            filter_['task__title__icontains'] = task
        if status_ := request.query_params.get('status'):
            status_ = status_.lower().capitalize()
            if status_ in statuses:
                filter_['status'] = statuses[status_]

        subtasks = subtasks.filter(**filter_)

        sort_by = request.query_params.get('sort_by', 'created_at').strip().lower()
        sort_order = request.query_params.get('order', 'desc').lower().strip()

        if sort_by not in self.ALLOWED_SORT_FIELDS:
            sort_by = 'created_at'

        if sort_order == 'desc':
            sort_by = f'-{sort_by}'

        subtasks = subtasks.order_by(sort_by)

        paginator = SubTaskPaginator()
        page = paginator.paginate_queryset(subtasks, request)

        if page is not None:
            serializer = SubTaskSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = SubTaskSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubTaskDetailUpdateDeleteView(APIView):

    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, partial=False):
        subtask = get_object_or_404(SubTask, pk=pk)
        serializer = SubTaskSerializer(subtask, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        return self.put(request, pk, partial=True)

    def delete(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

