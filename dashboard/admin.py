from django.contrib import admin
from . import models

admin.site.register(models.ChamaMembers)
admin.site.register(models.Chamas)
admin.site.register(models.Transactions)
admin.site.register(models.fieldID)
admin.site.register(models.TransactionTypes)
admin.site.register(models.Subscriptions)
admin.site.register(models.SubscriptionTypes)