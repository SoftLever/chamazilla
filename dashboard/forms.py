from django import forms
from . import models

class CreateUser(forms.ModelForm):
	class Meta:
		model = models.ChamaMembers
		fields = ['firstName', 'secondName']
		labels = {'firstName':'First Name', 'secondName': 'Second Name'}

class addTransaction(forms.ModelForm):
	class Meta:
		model = models.Transactions
		fields = ['memberID', 'transactionType', 'amount']
		labels = {'memberID': 'Member ID', 'transactionType': 'Transaction Type', 'amount': 'Amount'}