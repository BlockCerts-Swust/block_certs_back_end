# Generated by Django 3.0.3 on 2020-07-10 12:30

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0022_auto_20200710_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cert',
            name='create_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 10, 12, 30, 4, 197872, tzinfo=utc)),
        ),
    ]