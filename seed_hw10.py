import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.tasks.models import Task, SubTask
from apps.core.models import Statuses
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q, F

def create_task_obj():
    task_obj = Task.objects.create(
        title='Prepare presentation',
        description='Prepare materials and slides for the presentation',
        status=Statuses.NEW,
        deadline=timezone.now() + timedelta(days=3)
    )
    print(task_obj)

def create_few_subtasks():
    task = Task.objects.get(title='Prepare presentation',
                    description='Prepare materials and slides for the presentation')
    sub_obj_1 = SubTask(
        title="Gather information",
        task=task,
        description="Find necessary information for the presentation",
        status=Statuses.NEW,
        deadline=timezone.now() + timedelta(days=2)
    )
    sub_obj_2 = SubTask(
        title="Create slides",
        task=task,
        description="Create presentation slides",
        status=Statuses.NEW,
        deadline=timezone.now() + timedelta(days=1)
    )
    all_subtasks = SubTask.objects.bulk_create([sub_obj_1, sub_obj_2])

    print(all_subtasks)

# print(*(task for task in Task.objects.filter(status=Statuses.NEW)), sep='\n')
print(*Task.objects.filter(status=Statuses.NEW), sep='\n')
# print(*(subtask for subtask in
#         SubTask.objects.filter(Q(status=Statuses.DONE) & Q(deadline__lt=timezone.now()))), sep='\n')
print(*SubTask.objects.filter(status=Statuses.DONE, deadline__lt=timezone.now()), sep='\n')

def update_task():
    Task.objects.filter(title='Prepare presentation').update(status=Statuses.IN_PROGRESS)
    updated_task = Task.objects.get(title='Prepare presentation')
    print(f'Updated task: {updated_task}')

def update_subtasks():
    SubTask.objects.filter(title='Gather information').update(deadline=F('deadline') - timedelta(days=2))
    updated_deadline = SubTask.objects.get(title='Gather information')
    print(f'Updated deadline: {updated_deadline.deadline}')

    SubTask.objects.filter(title='Create slides').update(description='Create and format presentation slides')
    updated_description = SubTask.objects.get(title='Create slides')
    print(f'New description: {updated_description.description}')

def delete_task():
    deleted_count = Task.objects.get(title='Prepare presentation').delete()
    print(f'Total deleted: {deleted_count}')


if __name__ == '__main__':
    # create_task_obj()
    # create_few_subtasks()
    # update_task()
    # update_subtasks()
    # delete_task()
    pass

