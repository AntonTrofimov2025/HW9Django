from rest_framework import serializers
from apps.tasks.models import Task
from . import subtask
from django.utils import timezone
from apps.tasks.models import SubTask



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

class SubTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = SubTask
        fields = ['title', 'description', 'status', 'deadline', 'created_at', 'updated_at', 'task']
        read_only_fields = ['created_at', 'updated_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'subtasks']
        read_only_fields = ['subtasks']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']
        read_only_fields = ['id']

    def validate_deadline(self, value):
        now = timezone.now()
        if value < now:
            raise serializers.ValidationError('Deadline can not be in the past!')
        return value

