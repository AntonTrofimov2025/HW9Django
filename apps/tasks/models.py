from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from apps.core.models import UniqueId, Statuses
from django.utils import timezone
from django.db.models.functions import TruncDate
from apps.tasks.managers import CategorySoftDeleteManager



class Category(UniqueId):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(3)], verbose_name='Category name')
    deleted_at = models.DateTimeField(null=True, verbose_name=_('Deleted at'))

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    objects = CategorySoftDeleteManager()
    all_objects = models.Manager()

    def delete(self, *args, **kwargs):
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def __str__(self):
        return f'Category {self.name}'

    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name})>'

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        # unique_together = ('name', ) # obsolete, as I understood
        constraints = [models.UniqueConstraint(fields=['name'], name='unique_category_name',
                                               violation_error_message='Such a Category already exists!')]


class Task(UniqueId):
    title = models.CharField(max_length=25, validators=[MinLengthValidator(3)], verbose_name='Title')
                             # unique_for_date='created_at' NOT ACTUAL ALREADY BECAUSE OF UniqueConstraint
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

    class Meta:
        db_table = 'task_manager_task'
        ordering = ('-created_at',)
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        # unique_together = ('title', 'created_at') # obsolete, as I understood
        constraints = [
            models.UniqueConstraint('title', TruncDate('created_at'),
                                    name='unique_title_by_creation_date',
                                    violation_error_message='Such a Task already exists!')
        ]


class SubTask(UniqueId):
    title = models.CharField(max_length=25, validators=[MinLengthValidator(3)], verbose_name='Title')
    description = models.TextField(verbose_name="Subtask's description")
    task = models.ForeignKey('Task', related_name='subtasks', on_delete=models.CASCADE,
                                help_text="Subtask for the main task")
    status = models.CharField(max_length=12, choices=Statuses, verbose_name='Status')
    deadline = models.DateTimeField(verbose_name='DEADLINE')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def __str__(self):
        return f'Subtask {self.title}'

    def __repr__(self):
        return (f'SubTask(id={self.id}, title={self.title}, description={self.description},'
                f' status={self.status}, deadline={self.deadline}, created_at={self.created_at}, updated_at={self.updated_at})')

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ('-created_at',)
        verbose_name = _('SubTask')
        verbose_name_plural = _('SubTasks')
        # unique_together = ('title', 'created_at') # obsolete, as I understood
        constraints = [models.UniqueConstraint('title', TruncDate('created_at'),
                                             name='unique_subtask_title_by_creation_date',
                                             violation_error_message='Such a SubTask already exists!')]

