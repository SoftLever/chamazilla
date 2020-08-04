from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from dashboard.models import Chamas, Subscriptions

#CreateUserForm inherits from UserCreationForm
#The goal is to customize the registration form
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
		labels = {'username': 'Phone'}

class ChamaForm(forms.ModelForm):
	class Meta:
		model = Chamas
		fields = ['chamaName']

class SubscriptionForm(forms.ModelForm):
	class Meta:
		model = Subscriptions
		fields = ['subscriptionType']