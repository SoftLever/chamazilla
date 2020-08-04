from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import ChamaMembers, Transactions, Chamas, Subscriptions
from . import forms
from django.contrib.auth.decorators import login_required
from dashboard.decorators import userNotAuthenticated, userAuthenticated
import datetime
import math

@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def dashboard(request):
	session_chamaID = request.user.chamas.chamaID
	#for the transactions div
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")[:5]
	if not transactions:
		print("no records match")
	else:
		print("some records match")

	#for the basic info div
	members_count = ChamaMembers.objects.filter(chamaID = session_chamaID).count()
	chamaInfo = Chamas.objects.filter(chamaID = session_chamaID).last()

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
			chamaInfo = Chamas.objects.filter(chamaID = session_chamaID).last()
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
	form = forms.CreateUser()
	context = {'form': form}

	if request.method == 'POST':
		form = forms.CreateUser(request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			instance.chamaID = Chamas(chamaID = session_chamaID)#reference to a chama
			instance.save()
			print("New member added")
			#redirect('dashboard/members')
			return HttpResponseRedirect('members')

	return render(request, 'dashboard/membersForm.html', context)

#This view displays all chama members of the authenticated chama
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def members(request):
	session_chamaID = request.user.chamas.chamaID
	members_list = ChamaMembers.objects.filter(chamaID = session_chamaID).order_by("-memberID")

	context = {'members_list': members_list}

	return render(request, 'dashboard/chamaMembers.html', context)

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