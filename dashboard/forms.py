from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models

class addTransaction(forms.ModelForm):

	def __init__(self, chamaID, *args, **kwargs):
		super(addTransaction, self).__init__(*args, **kwargs)
		self.fields['memberID'] = forms.ModelChoiceField(queryset = models.ChamaMembers.objects.filter(chamaID = chamaID, user__is_active = True), empty_label = "Choose a member", widget = forms.Select(attrs = {'class':'form-control'}))

	class Meta:
		model = models.Transactions
		fields = ['memberID', 'transactionType', 'amount']
		labels = {'memberID': 'Member ID', 'transactionType': 'Transaction Type', 'amount': 'Amount'}
		widgets = {
			'amount':forms.NumberInput(attrs = {'class':'form-control'}),
			'transactionType':forms.Select(attrs = {'class':'form-control'}),
		}

class loanForm(forms.ModelForm):

	def __init__(self, chamaID, *args, **kwargs):
		super(loanForm, self).__init__(*args, **kwargs)
		self.fields['memberID'] = forms.ModelChoiceField(queryset = models.ChamaMembers.objects.filter(chamaID = chamaID, user__is_active = True), empty_label = "Choose a member", widget = forms.Select(attrs = {'class':'form-control'}))

	class Meta:
		model = models.Loans
		fields = ['memberID', 'amount']
		widgets = {
			'amount':forms.NumberInput(attrs = {'class': 'form-control'}),
		}