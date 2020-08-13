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

#for validations
from .formvalidations import phoneValidation

import datetime
import math

@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def dashboard(request):
	session_chamaID = request.user.chamas.chamaID
	#for the transactions div
	recentTransactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")[:5]
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("transactionDate")

	#Get only members who match the chama logged in and are active
	members_count = ChamaMembers.objects.filter(chamaID = session_chamaID, user__is_active = True).count()
	chamaInfo = request.user.chamas
	funds = 0
	for transaction in transactions:
		if str(transaction.transactionType) == "withdrawal":
			funds -= transaction.amount
		else:
			funds += transaction.amount

	#for the subscription div
	#get the last subscription because it's the relevant one
	subscription = Subscriptions.objects.filter(chamaID = session_chamaID).last()
	today = datetime.datetime.now(datetime.timezone.utc)#for checking if subscription is still active
	timeToExpiry = subscription.endDate - today
	daysToExpiry = timeToExpiry.days
	hoursToExpiry = math.floor(timeToExpiry.seconds/3600)
	minutesToExpiry = math.floor(((timeToExpiry.seconds % 3600)/60))
	
	context = {'recentTransactions': recentTransactions, 'chamaInfo':chamaInfo, 'funds': funds,
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

		#check if the amount is valid
		if int(request.POST.get('amount')) < 0:
			messages.warning(request, "Amount must be greater than 0")
			return HttpResponseRedirect('transactionsform')

		form = forms.addTransaction(session_chamaID, data = request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('transactions')

	return render(request, 'dashboard/transactionsForm.html', context)

#this view handles the members form
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def membersform(request):
	session_chamaID = request.user.chamas.chamaID

	if request.method == 'POST':
		username = request.POST.get('phone')
		password = username
		first_name = request.POST.get('first_name')
		last_name = request.POST.get('last_name')

		#if phone number is invalid
		if not phoneValidation(username):
			messages.warning(request, "Enter a phone number with format: 07********")
			#refresh the same page to display error
			return HttpResponseRedirect('membersform')

		#if the admin is trying to add themselves
		if username == request.user.username:
			try:
				ChamaMembers.objects.get(user__username = username)
				messages.warning(request, "You are already a member")
			except ChamaMembers.DoesNotExist:
				#set name as provided by admin
				request.user.first_name = first_name
				request.user.last_name = last_name

				#Create new chama member instance
				memberInstance = ChamaMembers(user = request.user, chamaID = Chamas(chamaID = session_chamaID))
				memberInstance.save()
				request.user.save()
				messages.success(request, "You added yourself to the group")
			except:
				messages.error(request, "Something went wrong")

			return HttpResponseRedirect('members')

		try:
			checkUser = ChamaMembers.objects.get(user__username = username)
			#check if user is active and is a member of this chama
			if checkUser.user.is_active == False and checkUser.chamaID.chamaID == session_chamaID:
				#change name of user who already exists
				checkUser.user.is_active = True
				checkUser.user.first_name = first_name
				checkUser.user.last_name = last_name

				checkUser.user.save()
				messages.success(request, "%s was added back to the group as %s %s" % (username, first_name, last_name))
			else:
				messages.warning(request, "%s already has a ChamaZilla account" %username)

		except ChamaMembers.DoesNotExist:
			#if the DoesNotExist error is raised, try to register the user
			try:
				newMember = User.objects.create_user(username, password = password, first_name = first_name, last_name = last_name)
			
				#add the user to chama member group
				group = Group.objects.get(name = "chama_member")
				newMember.groups.add(group)

				newMemberExtension = ChamaMembers(user = newMember, chamaID = Chamas(chamaID = session_chamaID))

				newMemberExtension.save()
				messages.success(request, "%s was added to the group" %username)
			except:
				messages.warning(request, "%s could not be added to the group" %username)
		
		#if some other error is raised
		except:
			messages.warning(request, "Something went wrong")
		
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

	try:
		#to prevent admins from deleting the group
		if request.user.username == username:
			messages.warning(request, "Call 0798380239 to change the group admin. Note: Changing admin will cost KSH30")
			return HttpResponseRedirect('/members')

		#to ensure a chama admin can disable only their members
		if session_chamaID == chamaID:
			user = User.objects.get(username = username)
			user.is_active = False
			user.save()
			messages.success(request, user.first_name + ' has been removed from ' + request.user.chamas.chamaName)
		else:
			messages.warning(request, 'Member does not exist')
	except:
		messages.warning(request, 'The member could not be deleted')

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
	#To know whether it's the group admin or 
	#member viewing this page
	viewingUser = request.user.groups.all()[0].name

	context = {}
	userInfo = ChamaMembers.objects.get(user__username = username)

	#if authorized member or authorized admin
	if request.user.username == username or request.user.username == userInfo.chamaID.user.username:
		userGroup = userInfo.user.groups.all()[0]

		#Show the user role without underscores
		userGroup = userGroup.name.replace("_", " ")
		transactions = Transactions.objects.filter(memberID = userInfo).order_by("-transactionDate")
		funds = 0;
		for transaction in transactions:
			if str(transaction.transactionType) == "withdrawal":
				funds -= transaction.amount

			#fines are added to the chama's funds, not members
			elif str(transaction.transactionType) == "fine":
				funds +=0
			else:
				funds += transaction.amount

		context = {"viewingUser":viewingUser, "userInfo": userInfo, "userGroup": userGroup, "transactions": transactions, "funds": funds}
	else:
		return HttpResponse('You are not authorized to view this page')

	return render(request, 'dashboard/memberPage.html', context)