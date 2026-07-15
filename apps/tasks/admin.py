from django.contrib import admin
from .models import Category, Task, SubTask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('-name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'description', 'status', 'deadline')
    list_editable = ('description', 'status', 'deadline')
    ordering = ('-title',)
    search_fields = ('title',)


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'description', 'status', 'deadline')
    list_editable = ('description', 'status', 'deadline')
    ordering = ('-title',)
    search_fields = ('title',)




