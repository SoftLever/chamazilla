from django.contrib import admin
from .models import ChamaMembers, Chamas, Transactions, fieldID, TransactionTypes

admin.site.register(ChamaMembers)
admin.site.register(Chamas)
admin.site.register(Transactions)
admin.site.register(fieldID)
admin.site.register(TransactionTypes)