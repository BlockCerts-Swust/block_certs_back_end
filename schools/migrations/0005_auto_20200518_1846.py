# Generated by Django 3.0.3 on 2020-05-18 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0004_revocation_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revocation',
            name='public_key',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterUniqueTogether(
            name='revocation',
            unique_together={('uuid', 'public_key')},
        ),
    ]
