# Generated by Django 3.0.3 on 2020-07-10 11:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_auto_20200710_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cert',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 10, 11, 42, 55, 784108, tzinfo=utc)),
        ),
    ]
