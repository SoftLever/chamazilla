from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import ChamaMembers, Transactions, Chamas, Subscriptions
from . import forms

#for confirming deletion of users
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from dashboard.decorators import userNotAuthenticated, userAuthenticated

#For handling member information
from django.contrib.auth.models import User

#To place chama members into their group
from django.contrib.auth.models import Group

import datetime
import math

@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def dashboard(request):
	session_chamaID = request.user.chamas.chamaID
	#for the transactions div
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")[:5]

	#Get only members who match the chama logged in and are active
	members_count = ChamaMembers.objects.filter(chamaID = session_chamaID, user__is_active = True).count()
	chamaInfo = request.user.chamas

	#for the subscription div
	#get the last subscription because it's the relevant one
	subscription = Subscriptions.objects.filter(chamaID = session_chamaID).last()
	today = datetime.datetime.now(datetime.timezone.utc)#for checking if subscription is still active
	timeToExpiry = subscription.endDate - today
	daysToExpiry = timeToExpiry.days
	hoursToExpiry = math.floor(timeToExpiry.seconds/3600)
	minutesToExpiry = math.floor(((timeToExpiry.seconds % 3600)/60))
	
	context = {'transactions': transactions, 'chamaInfo': chamaInfo,
	'members_count': members_count, 'subscription': subscription,
	'today': today, 'daysToExpiry': daysToExpiry, 'hoursToExpiry': hoursToExpiry,
	'minutesToExpiry': minutesToExpiry}

	return render(request, 'dashboard/dashboard.html', context)

#this view handles the transactions form
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def transactionsform(request):
	session_chamaID = request.user.chamas.chamaID
	form = forms.addTransaction(session_chamaID)
	context = {'form': form}
	if request.method == 'POST':
		form = forms.addTransaction(session_chamaID, data = request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			print(instance.amount)

			#update the total funds of the chama
			chamaInfo = request.user.chamas
			if str(instance.transactionType) == "withdrawal":
				chamaInfo.funds -= instance.amount
			else:
				chamaInfo.funds += instance.amount
			instance.save()
			chamaInfo.save()
			print("New Transaction recorded, funds updated")
			return HttpResponseRedirect('transactions')

	return render(request, 'dashboard/transactionsForm.html', context)

#this view handles the members form
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def membersform(request):
	session_chamaID = request.user.chamas.chamaID

	if request.method == 'POST':
		username = request.POST.get('phone')
		#password defaults to the phone number given
		password = username
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')

		newMember = User.objects.create_user(username, password = password, first_name = first_name, last_name = last_name)
		
		#add the user to chama member group
		group = Group.objects.get(name = "chama_member")
		newMember.groups.add(group)

		newMemberExtension = ChamaMembers(user = newMember, chamaID = Chamas(chamaID = session_chamaID))

		newMemberExtension.save()
		return HttpResponseRedirect('members')

	return render(request, 'dashboard/membersForm.html')

#This view displays all chama members of the authenticated chama
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def members(request):
	session_chamaID = request.user.chamas.chamaID
	members_list = ChamaMembers.objects.filter(chamaID = session_chamaID, user__is_active = True).order_by("-memberID")

	context = {'members_list': members_list}

	return render(request, 'dashboard/chamaMembers.html', context)

#Member deletion view
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def deleteUser(request, chamaID = None, username = None):
	#we get username and their chama from urls
	session_chamaID = request.user.chamas.chamaID

	#to ensure a chama admin can disable only their members
	if session_chamaID == chamaID:
		user = User.objects.get(username = username)
		user.is_active = False
		user.save()
		messages.success(request, user.first_name + ' has been removed from ' + request.user.chamas.chamaName)
	else:
		messages.warning(request, 'Member does not exist')

	return HttpResponseRedirect('/members')

#This view displays all transactions of the authenticated chama
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def transactions(request):
	session_chamaID = request.user.chamas.chamaID
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")

	context = {'transactions': transactions}

	return render(request, 'dashboard/transactions.html', context)

@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def loans(request):
	return render(request, 'dashboard/loans.html')

#This view displays individual chama member information
#Should be accessible to the relevant member only and their admin
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_member', 'chama_admin'])
def memberPage(request, username =None):
	context = {}
	userInfo = ChamaMembers.objects.get(user__username = username)
	print(userInfo.chamaID.chamaName)

	#if authorized member or authorized admin
	if request.user.username == username or request.user.username == userInfo.chamaID.user.username:
		userGroup = userInfo.user.groups.all()[0]

		#Show the user role without underscores
		userGroup = userGroup.name.replace("_", " ")
		transactions = Transactions.objects.filter(memberID = userInfo)
		context = {"userInfo": userInfo, "userGroup": userGroup, "transactions": transactions}
	else:
		return HttpResponse('You are not authorized to view this page')

	return render(request, 'dashboard/memberPage.html', context)