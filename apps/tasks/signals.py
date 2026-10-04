from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models import Task
from apps.core.models import Statuses
from django.core.mail import send_mail
from django.conf import settings

@receiver(pre_save, sender=Task, dispatch_uid='task_st_changed')
def task_status_changed(sender, instance, **kwargs):
    try:
        task = Task.objects.get(pk=instance.id)
    except Task.DoesNotExist:
        return
    if instance.status != task.status:
        if not instance.owner or not instance.owner.email:
            return
        if instance.status == Statuses.DONE:
            msg = "It's DONE! Task has been successfully closed! :)"
        else:
            msg = f"Task status changed from {task.status} to {instance.status}"
        send_mail(
            subject="New Task Status",
            message=msg,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.owner.email]
        )