# Generated by Django 3.0.7 on 2020-08-09 16:04

import dashboard.models
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChamaMembers',
            fields=[
                ('memberID', models.CharField(default=dashboard.models.generate_memberID, max_length=15, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Chamas',
            fields=[
                ('chamaID', models.CharField(default=dashboard.models.generate_ChamaID, max_length=15, primary_key=True, serialize=False)),
                ('chamaName', models.CharField(max_length=50)),
                ('regDate', models.DateTimeField(auto_now_add=True)),
                ('funds', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='fieldID',
            fields=[
                ('fieldName', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('currentNumber', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionTypes',
            fields=[
                ('subscriptionType', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='TransactionTypes',
            fields=[
                ('transactionType', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('transactionID', models.CharField(default=dashboard.models.generate_TransactionID, max_length=20, primary_key=True, serialize=False)),
                ('transactionDate', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('memberID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ChamaMembers')),
                ('transactionType', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.TransactionTypes')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('subscriptionID', models.CharField(default=dashboard.models.generate_SubscriptionID, max_length=20, primary_key=True, serialize=False)),
                ('startDate', models.DateTimeField(auto_now_add=True)),
                ('endDate', models.DateTimeField(default=datetime.datetime(2020, 8, 16, 16, 4, 4, 484699))),
                ('amount', models.IntegerField(default=0)),
                ('chamaID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Chamas')),
                ('subscriptionType', models.ForeignKey(default='trial', on_delete=django.db.models.deletion.CASCADE, to='dashboard.SubscriptionTypes')),
            ],
        ),
        migrations.AddField(
            model_name='chamamembers',
            name='chamaID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Chamas'),
        ),
        migrations.AddField(
            model_name='chamamembers',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
