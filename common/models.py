# Create your models here.
import datetime

from django.utils import timezone
from mongoengine import FileField, StringField, Document, DateTimeField
from django.db import models


class File(Document):
    wsid = StringField(required=True, max_length=100, primary_key=True)
    name = StringField(required=True, max_length=100)
    file = FileField(required=True)
    file_detail_url = StringField(required=True)
    file_download_url = StringField(required=True)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True

class Cert(models.Model):
    cert_image_wsid = models.CharField(max_length=100, unique=True)
    certificate_description = models.CharField(max_length=255)
    certificate_title = models.CharField(max_length=255)
    criteria_narrative = models.CharField(max_length=588)
    cert_id = models.CharField(max_length=255)
    student_name = models.CharField(max_length=255)
    student_pubkey = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    school_pubkey = models.CharField(max_length=255)
    status = models.IntegerField(default=0)
    create_time = models.DateTimeField(default=datetime.datetime.now)