# Generated by Django 3.0.7 on 2020-08-01 23:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0012_auto_20200801_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chamas',
            name='chamaName',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='subscriptions',
            name='endDate',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 31, 23, 28, 18, 308696)),
        ),
    ]
