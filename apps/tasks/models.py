from django.db import models
from django.core.validators import MinLengthValidator
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _
from apps.core.models import UniqueId
from django.utils import timezone



class Statuses(TextChoices):
    NEW = 'new', _('New')
    IN_PROGRESS = 'in_progress', _('In progress')
    PENDING = 'pending', _('Pending')
    BLOCKED = 'blocked', _('Blocked')
    DONE = 'done', _('Done')



class Category(UniqueId):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)], verbose_name='Category name')

    def __str__(self):
        return f'Category {self.name}'

    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name})>'


class Task(UniqueId):
    title = models.CharField(max_length=25, validators=[MinLengthValidator(3)], verbose_name='Title',
                             unique_for_date='created_at')
    # created_at = models.DateTimeField(default=timezone.now, verbose_name='Creation date')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    description = models.TextField(verbose_name="Task's description")
    categories = models.ManyToManyField('Category', related_name='tasks', help_text="Category for every task")
    status = models.CharField(max_length=12, choices=Statuses, verbose_name='Status')
    deadline = models.DateTimeField(verbose_name='DEADLINE')

    def __str__(self):
        return f'Task {self.title}'

    def __repr__(self):
        return (f'<Task(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})>')


class SubTask(UniqueId):
    title = models.CharField(max_length=25, validators=[MinLengthValidator(3)], verbose_name='Title')
    description = models.TextField(verbose_name="Subtask's description")
    task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE,
                                help_text="Subtask for the main task")
    status = models.CharField(max_length=12, choices=[('new', 'New'), ('in_progress', 'In progress'),
                                       ('pending', 'Pending'), ('blocked', 'Blocked'),
                                       ('done', 'Done')], verbose_name='Status')
    deadline = models.DateTimeField(verbose_name='DEADLINE')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return f'Subtask {self.title}'

    def __repr__(self):
        return (f'SubTask(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})')

