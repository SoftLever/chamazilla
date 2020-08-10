from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from dashboard.decorators import userNotAuthenticated
from dashboard.models import Chamas

def index(request):
	return render(request, 'member_records/index.html')

#Redirect the user if they are already authenticated
@userNotAuthenticated
def signup(request):
	form = forms.CreateUserForm()
	chamaForm = forms.ChamaForm()
	subscriptionForm = forms.SubscriptionForm()

	if request.method == "POST":
		form = forms.CreateUserForm(request.POST)
		chamaForm = forms.ChamaForm(request.POST)
		subscriptionForm = forms.SubscriptionForm(request.POST)
		#and subscriptionForm.is_valid
		if form.is_valid() and chamaForm.is_valid() and subscriptionForm.is_valid():

			#Save the user
			user = form.save()

			#Add the user to chama admin group
			group = Group.objects.get(name = "chama_admin")
			user.groups.add(group)

			#Create a chama
			chama = chamaForm.save(commit = False)
			chama.user = user

			#Add subscription for chama
			subscription = subscriptionForm.save(commit = False)
			subscription.chamaID = chama

			chama = chama.save()
			subscription.save()

			messages.success(request, 'Account was created successfully')
			messages.success(request, 'Your payment quote will be sent in 24 hours')
			return redirect('login')

	context = {'form':form, 'chamaForm':chamaForm, 'subscriptionForm':subscriptionForm}

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