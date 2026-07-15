from django.db import models
import uuid

class UniqueId(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False, help_text='Unique uuid id', verbose_name='UUID id')
    class Meta:
        abstract = True
