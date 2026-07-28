from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.tasks.models import Task, Statuses
from apps.tasks.serializers import TaskSerializer
from django.db.models import Count, Q
from django.utils import timezone


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def tasks_requests(request, id_=None):
    if request.method == 'GET' and id_ is not None:
        try:
            task = Task.objects.get(id=id_)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response({'Task found': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f"New Task {serializer.validated_data['title']} has been successfully added! :)"},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method in ['PUT', 'PATCH']:
        if id_ is None:
            return Response({'error': 'Methods PUT PATCH require an ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(id=id_)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        is_partial = request.method == 'PATCH'

        serializer = TaskSerializer(task, data=request.data, partial=is_partial)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': f"Task {serializer.data['title']} has been successfully updated! :D",
                             'updated_task': serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if id_ is None:
            return Response({'error': 'Method DELETE requires an ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            task = Task.objects.get(id=id_)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

        task.delete()
        return Response({'msg': f'Task ({id_}) has been successfully deleted!'}, status=status.HTTP_200_OK)

# @api_view(['GET'])
# def tasks_by_status(request, status_):
#     statuses = {status__.label: status__.value for status__ in Statuses}
#     if request.method == 'GET' and status_ is not None and status_ in statuses:
#         tasks_by_st = Task.objects.filter(status=statuses[status_]).aggregate(tasks_count=Count('id'))['tasks_count']
#         return Response({f'Found tasks by status {status_}': tasks_by_st}, status=status.HTTP_200_OK)
#     else:
#         return Response({'msg': 'This status not found :('}, status=status.HTTP_404_NOT_FOUND)
#
# @api_view(['GET'])
# def tasks_count_all(request):
#     if request.method == 'GET':
#         tasks_count = Task.objects.aggregate(tasks_count=Count('id'))['tasks_count'] # OR JUST Task.objects.all().count()
#         return Response({'Tasks found': tasks_count}, status=status.HTTP_200_OK)     # MUCH EASIER :)
#
# @api_view(['GET'])
# def tasks_expired_date(request):
#     if request.method == 'GET':
#         now = timezone.now()
#         expired_tasks_count = Task.objects.filter(deadline__lt=now).count()
#         return Response({'Expired tasks': expired_tasks_count}, status=status.HTTP_200_OK)


@api_view(['GET'])
def tasks_aggregate_all(request):
    if request.method == 'GET':
        now = timezone.now()
        tasks_aggregation = Task.objects.aggregate(total_count=Count('id'),
                                                   expired_tasks=Count('id', filter=Q(deadline__lt=now)),
        **{f'{status__.value}_count': Count('id', filter=Q(status=status__.value)) for status__ in Statuses})
        return Response({'Statistics': tasks_aggregation}, status=status.HTTP_200_OK)

