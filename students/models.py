import binascii
import datetime
import os
import uuid

from django.db import models
from students.hashers import make_password
from mongoengine import DynamicDocument, ListField, StringField, DictField, DateTimeField


# Create your models here.

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=128, unique=True)
    student_num = models.CharField(max_length=128, unique=True)
    chain_address = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=225)
    register_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name, self.last_name

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class StudentToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    student = models.OneToOneField(to='Student', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

class UnsignCert(DynamicDocument):
    wsid = StringField(default="cert_wsid_" + str(uuid.uuid4()), primary_key=True)
    data = DictField()