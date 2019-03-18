# Generated by Django 2.0.6 on 2019-03-14 14:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wikipediaApp', '0004_auto_20190314_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 14, 14, 52, 28, 134218, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='article',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 14, 14, 52, 28, 134243, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='related',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 14, 14, 52, 28, 134952, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='related',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 14, 14, 52, 28, 134974, tzinfo=utc)),
        ),
    ]