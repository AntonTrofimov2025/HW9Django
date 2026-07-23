from django.contrib import admin
from .models import Category, Task, SubTask, Statuses


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-name',)


class SubTaskInline(admin.StackedInline):
    model = SubTask
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'created_at', 'updated_at', 'description', 'status', 'deadline')
    list_editable = ('description', 'status', 'deadline')
    ordering = ('-title',)
    search_fields = ('title',)
    inlines = [SubTaskInline]

    @admin.display(description='Title')
    def short_title(self, task):
        if task.title and len(task.title) > 10:
            return f'{task.title[:10]}...'
        return task.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'description', 'status', 'deadline')
    list_editable = ('description', 'status', 'deadline')
    ordering = ('-title',)
    search_fields = ('title',)

    @admin.action(description="Set SubTask's status to DONE")
    def change_status_to_done(self, request, subtasks):
        # for subtask in subtasks:
        #     subtask.status = Statuses.DONE
        #     subtask.save()
        subtasks.update(status=Statuses.DONE)

    actions = [change_status_to_done]

