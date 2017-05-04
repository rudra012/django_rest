# -*- coding: utf-8 -*-

# Standard Library
import uuid
from io import BytesIO

# Third Party Stuff
from PIL import Image as Img
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django_extensions.db.models import TimeStampedModel
from uuid_upload_path import upload_to
from versatileimagefield.fields import PPOIField, VersatileImageField
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import certifi
from rest_framework import exceptions
def compress_image(image_object, image_quality=settings.IMAGE_QUALITY):
    """
    To compress any image file.
    :param image_object: Image object to be compress
    :param image_quality: quality of image after compression
    :return: Compressed image object
    """
    image_object.open()
    img = Img.open(BytesIO(image_object.read()))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    basewidth=settings.IMAGE_BASE_WIDTH
    if basewidth >= image_object.width:
        img.thumbnail((image_object.width, image_object.height), Img.ANTIALIAS)
    else:
        wpercent=(basewidth / float(img.size[0]))
        hsize=int((float(img.size[1]) * float(wpercent)))
        img.thumbnail((basewidth,hsize), Img.ANTIALIAS)

    # print("%d , %d " % (img.size[0],img.size[1]))
    output = BytesIO()
    img.save(output, format='JPEG', quality=image_quality)
    output.seek(0)
    return InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image_object.name.split('.')[0],
                                'image/jpeg',
                                output.__sizeof__(), None)


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


class ImageMixin(models.Model):
    '''
    An abstract base class model that provides a VersatileImageField Image with POI
    '''

    image = VersatileImageField(upload_to=upload_to, blank=True, null=True, ppoi_field='image_poi',
                                verbose_name="image")
    image_poi = PPOIField(verbose_name="image's Point of Interest")  # point of interest

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.image:
            self.image = compress_image(self.image)
        super(ImageMixin, self).save(*args, **kwargs)


class ElasticSearchWrapper:
    def __init__(self):
        self.es = Elasticsearch(
            [settings.ELASTICSEARCH_URL], port=settings.ELASTICSEARCH_PORT,
            http_auth=settings.ELASTICSEARCH_USERNAME+":"+settings.ELASTICSEARCH_PASSWORD,
            use_ssl=True,
            verify_certs=True,
            ca_certs=certifi.where()
        )

    def save(self,doc_type,body,id):
        try:
            self.es.index(index=settings.ELASTICSEARCH_INDEX, doc_type=doc_type, body=body,id=doc_type+"-"+id)
        except RequestError as e:
            raise exceptions.APIException(e.error)

    def save_bulk(self,body):
        try:
            self.es.bulk(body=body, index=settings.ELASTICSEARCH_INDEX)
        except RequestError as e:
            raise exceptions.APIException(e.info)
