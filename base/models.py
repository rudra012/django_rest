# -*- coding: utf-8 -*-

# Standard Library
import uuid

from django.db import models
from django_extensions.db.models import TimeStampedModel


class UUIDModel(models.Model):
    '''
    An abstract base class model that makes primary key `id` as UUID
    instead of default auto incremented number.
    '''
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class TimeStampedUUIDModel(TimeStampedModel, UUIDModel):
    '''
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields with UUID as primary_key field.
    '''

    class Meta:
        abstract = True
