# Generated by Django 3.0.7 on 2020-09-08 20:01

import dashboard.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_auto_20200822_2157'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoanStatus',
            fields=[
                ('loanStatusID', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Loans',
            fields=[
                ('loanID', models.CharField(default=dashboard.models.generate_loanID, max_length=30, primary_key=True, serialize=False)),
                ('amount', models.IntegerField(default=0)),
                ('issueDate', models.DateTimeField(default=django.utils.timezone.now)),
                ('repaymentDate', models.DateTimeField(default=dashboard.models.set_Repayment_Date)),
                ('memberID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.ChamaMembers')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.LoanStatus')),
            ],
        ),
    ]
