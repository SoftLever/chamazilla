from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from dashboard.models import Chamas, Subscriptions

#CreateUserForm inherits from UserCreationForm
#The goal is to customize the registration form
class CreateUserForm(UserCreationForm):

	#customize password validation text
	error_messages = {
		"password_mismatch":"The passwords don't match."
	}

	#override the password1 and password2 widgets
	password1 = forms.CharField(
	    widget=forms.PasswordInput(attrs={'class':'signup_input','autocomplete':'new-password','form':'signup_form', 'id':'password1', 'placeholder':'Type a password...'}),
	)
	password2 = forms.CharField(
	    widget=forms.PasswordInput(attrs={'class':'signup_input','autocomplete':'new-password','form':'signup_form', 'id':'password2', 'placeholder':'Type password again...'}),
	)

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
		widgets = {
			'username':forms.TextInput(attrs = {'class':'signup_input', 'form':'signup_form', 'id':'phone_number', 'placeholder':'07XXXXXXXX'}),
		}

class ChamaForm(forms.ModelForm):
	class Meta:
		model = Chamas
		fields = ['chamaName']
		widgets = {
			'chamaName':forms.TextInput(attrs = {'autofocus':'','class':'signup_input', 'form':'signup_form', 'id':'chamaName', 'placeholder':'Type the group name here...'})
		}