import binascii
import os
from django.db import models
from students.hashers import make_password
# Create your models here.

class School(models.Model):
    context = models.CharField(max_length=255, default=[
    "https://w3id.org/openbadges/v2",
    "https://w3id.org/blockcerts/v2"
  ])
    type = models.CharField(default="Profile", max_length=128)
    name = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=128, unique=True)
    official_website = models.CharField(max_length=255, unique=True)
    id_url = models.CharField(max_length=255, unique=True)
    revocation_list = models.CharField(max_length=255, unique=True)
    introduction_url = models.CharField(max_length=255, unique=True)
    public_key = models.CharField(max_length=128, unique=True)
    job_title = models.CharField(max_length=128)
    signature_name = models.CharField(max_length=128)
    signature_file_wsid = models.CharField(max_length=128)
    logo_file_wsid = models.CharField(max_length=128)
    password = models.CharField(max_length=225)
    register_date = models.DateTimeField(auto_now=True)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password


class SchoolToken(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    school = models.OneToOneField(to='School', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

class Revocation(models.Model):
    uuid = models.CharField(max_length=128)
    revocationReason = models.CharField(max_length=128)
    public_key = models.CharField(max_length=128, unique=True)
    created_time = models.DateTimeField(auto_now=True)