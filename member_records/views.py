from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from dashboard.decorators import userNotAuthenticated
from dashboard.models import Chamas, Subscriptions, LoanSettings

#for validating signup form
from dashboard.formvalidations import phoneValidation

def index(request):
	return render(request, 'member_records/index.html')

def api(request):
	return render(request, 'member_records/api.html')

#Redirect the user if they are already authenticated
@userNotAuthenticated
def signup(request):
	form = forms.CreateUserForm()
	chamaForm = forms.ChamaForm()

	if request.method == "POST":
		#Check if the phone number is valid
		if not phoneValidation(request.POST.get('username')):
			messages.warning(request, 'Enter phone number with this format: 07********')
			return HttpResponseRedirect('signup')

		form = forms.CreateUserForm(request.POST)
		chamaForm = forms.ChamaForm(request.POST)
		if form.is_valid() and chamaForm.is_valid():

			#Save the user
			user = form.save()

			#Add the user to chama admin group
			group = Group.objects.get(name = "chama_admin")
			user.groups.add(group)

			#Create a chama
			chama = chamaForm.save(commit = False)
			chama.user = user

			#Add subscription for chama
			subscription = Subscriptions(chamaID = chama)

			#Add default loan settings for chama
			loanSettings = LoanSettings(chamaID = chama)

			chama.save()
			subscription.save()
			loanSettings.save()

			messages.success(request, 'Account was created successfully.')
			return redirect('login')

	context = {'form':form, 'chamaForm':chamaForm}

	return render(request, 'member_records/signup.html', context)

@userNotAuthenticated
def loginpage(request):
	if request.method == "POST":
		username = request.POST.get('phone')
		password = request.POST.get('password')
		user = authenticate(username = username, password = password)

		if user is not None:
			login(request, user)
			#redirect user depending on role
			if user.groups.all()[0].name == "chama_admin":
				return redirect('dashboard')
			elif user.groups.all()[0].name == "chama_member":
				return redirect('memberpage/%s/' % user.username)
			else:
				#if user doesn't belong to any group, meme them
				return redirect('https://bit.ly/2PANTtD')
		else:
			messages.info(request, 'Username or password is incorrect')

	return render(request, 'member_records/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')