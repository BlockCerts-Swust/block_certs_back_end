# Generated by Django 3.0.3 on 2020-05-22 07:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_auto_20200430_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cert',
            name='cert_id',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='cert',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 22, 7, 30, 46, 942127, tzinfo=utc)),
        ),
    ]
