from rest_framework import serializers
from apps.tasks.models import Task
from . import subtask
from django.utils import timezone
from apps.tasks.models import SubTask



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'owner']
        read_only_fields = ['created_at', 'updated_at', 'owner']

class SubTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer(read_only=True)

    class Meta:
        model = SubTask
        fields = ['title', 'description', 'status', 'deadline', 'created_at', 'updated_at', 'task', 'owner']
        read_only_fields = ['created_at', 'updated_at', 'owner']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'subtasks', 'owner']
        read_only_fields = ['subtasks', 'owner']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'owner']
        read_only_fields = ['id', 'owner']

    def validate_deadline(self, value):
        now = timezone.now()
        if value < now:
            raise serializers.ValidationError('Deadline can not be in the past!')
        return value

