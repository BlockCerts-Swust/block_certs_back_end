# Create your models here.
from mongoengine import DynamicDocument, DictField
from mongoengine import DateTimeField as mongoengine_DateTimeField
from django.utils import timezone
from mongoengine import FileField, StringField, Document, DateTimeField
from django.db import models
import uuid


class File(Document):
    wsid = StringField(required=True, max_length=100, primary_key=True)
    name = StringField(required=True, max_length=100)
    file = FileField(required=True)
    file_detail_url = StringField(required=True)
    file_download_url = StringField(required=True)
    create_time = DateTimeField(default=timezone.now())

    class Meta:
        abstract = True

class Cert(models.Model):
    cert_image_wsid = models.CharField(max_length=100, unique=True)
    certificate_description = models.CharField(max_length=255)
    certificate_title = models.CharField(max_length=255)
    criteria_narrative = models.CharField(max_length=588)
    cert_id = models.CharField(max_length=255, unique=True)
    student_name = models.CharField(max_length=255)
    student_pubkey = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    school_pubkey = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    # status=0 create
    # status=1 issued
    # status=2 issuing
    # status=3 issue fail
    # status=4 revoked
    # status=5 refuse
    status = models.IntegerField(default=0)
    txid = models.CharField(max_length=255, blank=True)
    chain = models.CharField(max_length=255, blank=True)
    create_time = models.DateTimeField(default=timezone.now())
    refuse_reason = models.CharField(max_length=255, blank=True)


class CertDetail(DynamicDocument):
    wsid = StringField(primary_key=True)
    unsign_cert = DictField()
    sign_cert = DictField()
    block_cert = DictField()
    create_time = mongoengine_DateTimeField(default=timezone.now())
