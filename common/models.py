# Create your models here.
import datetime

from mongoengine import FileField, StringField, Document, DateTimeField


class File(Document):
    wsid = StringField(required=True, max_length=100, primary_key=True)
    name = StringField(required=True, max_length=100)
    file = FileField(required=True)
    file_detail_url = StringField(required=True)
    file_download_url = StringField(required=True)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True