from django.contrib import admin
from . import models

admin_models = [models.ChamaMembers, models.Chamas, models.Transactions, models.fieldID, models.TransactionTypes, models.Subscriptions, models.SubscriptionTypes, models.Loans, models.LoanSettings, models.LoanStatus]
admin.site.register(admin_models)