# Create your models here.
import datetime

from mongoengine import FileField, StringField, Document, DateTimeField


class File(Document):
    wsid = StringField(max_length=100, primary_key=True)
    name = StringField(max_length=100)
    file = FileField()
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        abstract = True