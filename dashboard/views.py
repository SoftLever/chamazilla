from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import ChamaMembers, Transactions, Chamas, Subscriptions
from . import forms
import datetime

session_chamaID = "CSG00004"

def dashboard(request):
	#for the transactions div
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")[:5]

	#for the basic info div
	members_count = ChamaMembers.objects.filter(chamaID = session_chamaID).count()
	chamaInfo = Chamas.objects.filter(chamaID = session_chamaID).last()

	#for the subscription div
	#get the last subscription because it's the relevant one
	subscription = Subscriptions.objects.filter(chamaID = session_chamaID).last()
	daysToExpiry = subscription.endDate - subscription.startDate
	today = datetime.datetime.now()#for checking if subscription is still active

	context = {'transactions': transactions, 'chamaInfo': chamaInfo, 'members_count': members_count, 'subscription': subscription, 'today': today, 'daysToExpiry': daysToExpiry}

	return render(request, 'dashboard/dashboard.html', context)

#this view handles the transactions form
def transactionsform(request):
	form = forms.addTransaction()
	context = {'form': form}
	if request.method == 'POST':
		form = forms.addTransaction(request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			print(instance.amount)

			#update the total funds of the chama
			chamaInfo = Chamas.objects.filter(chamaID = session_chamaID).last()
			chamaInfo.funds += instance.amount
			instance.save()
			chamaInfo.save()
			print("New Transaction recorded, funds updated")
			return HttpResponseRedirect('transactions')

	return render(request, 'dashboard/transactionsForm.html', context)

#this view handles the members form
def membersform(request):
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
def members(request):
	members_list = ChamaMembers.objects.filter(chamaID = session_chamaID).order_by("-memberID")

	context = {'members_list': members_list}

	return render(request, 'dashboard/chamaMembers.html', context)

#This view displays all transactions of the authenticated chama
def transactions(request):
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")

	context = {'transactions': transactions}

	return render(request, 'dashboard/transactions.html', context)

def loans(request):
	return render(request, 'dashboard/loans.html')