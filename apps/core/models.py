from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _


class UniqueId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, help_text='Unique uuid id', verbose_name='UUID id')
    class Meta:
        abstract = True


class Statuses(models.TextChoices):
    NEW = 'new', _('New')
    IN_PROGRESS = 'in_progress', _('In progress')
    PENDING = 'pending', _('Pending')
    BLOCKED = 'blocked', _('Blocked')
    DONE = 'done', _('Done')