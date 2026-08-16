from rest_framework import serializers
from apps.tasks.models import SubTask


# class SubTaskSerializer(serializers.ModelSerializer):
#     task = task.TaskSerializer(read_only=True)
#
#     class Meta:
#         model = SubTask
#         fields = ['title', 'description', 'status', 'deadline', 'created_at', 'updated_at', 'task']
# MOVED to task.py because of circular problem

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['title', 'description', 'status', 'deadline', 'created_at', 'updated_at']
        read_only_fields = ['id']
