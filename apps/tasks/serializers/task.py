from rest_framework import serializers
from apps.tasks.models import Task
from .subtask import SubTaskSerializer
from django.utils import timezone



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline', 'subtasks']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'deadline']

    def validate_deadline(self, value):
        now = timezone.now()
        if value < now:
            raise serializers.ValidationError('Deadline can not be in the past!')
        return value

