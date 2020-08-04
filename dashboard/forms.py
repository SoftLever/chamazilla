from django import forms
from . import models

class CreateUser(forms.ModelForm):
	class Meta:
		model = models.ChamaMembers
		fields = ['firstName', 'secondName']
		labels = {'firstName':'First Name', 'secondName': 'Second Name'}

class addTransaction(forms.ModelForm):

	def __init__(self, chamaID, *args, **kwargs):
		super(addTransaction, self).__init__(*args, **kwargs)
		self.fields['memberID'] = forms.ModelChoiceField(queryset = models.ChamaMembers.objects.filter(chamaID = chamaID), empty_label = "Choose a member")

	class Meta:
		model = models.Transactions
		fields = ['memberID', 'transactionType', 'amount']
		labels = {'memberID': 'Member ID', 'transactionType': 'Transaction Type', 'amount': 'Amount'}