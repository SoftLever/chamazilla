from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import ChamaMembers, Transactions, Chamas, Subscriptions, LoanSettings, Loans
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

#to paginate data so that table doesn't get too long
from django.core.paginator import Paginator

import datetime
import math

#to set loans repayment date
from django.utils import timezone

#most common tasks
def calculateChamaFunds(chama):
	funds = 0
	totalLoans = 0
	totalTransactions = 0

	transactions = Transactions.objects.filter(memberID__chamaID = chama)
	loans = Loans.objects.filter(memberID__chamaID = chama)

	for loan in loans:
		totalLoans += loan.amount

	for transaction in transactions:
		if str(transaction.transactionType) == "withdrawal":
			totalTransactions -= transaction.amount
		else:
			totalTransactions += transaction.amount

	funds = totalTransactions - totalLoans

	return funds

def calculateMemberFunds(member):
	transactions = Transactions.objects.filter(memberID = member).order_by("-transactionDate")
	funds = 0;
	for transaction in transactions:
		if str(transaction.transactionType) == "withdrawal":
			funds -= transaction.amount

		#fines are added to the chama's funds, not members
		#This logic may vary for each chama
		elif str(transaction.transactionType) == "fine":
			funds -= transaction.amount
		else:
			funds += transaction.amount

	return funds

@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def dashboard(request):
	session_chamaID = request.user.chamas.chamaID
	#for the transactions div
	recentTransactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")[:10]
	numberOfTransactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).count()

	#Get only members who match the chama logged in and are active
	members_count = ChamaMembers.objects.filter(chamaID = session_chamaID, user__is_active = True).count()
	chamaInfo = request.user.chamas

	#Calculate funds
	funds = calculateChamaFunds(session_chamaID)

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
	'minutesToExpiry': minutesToExpiry, 'numberOfTransactions': numberOfTransactions}

	return render(request, 'dashboard/dashboard.html', context)

#this view handles the transactions form
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def transactionsform(request):
	session_chamaID = request.user.chamas.chamaID
	#calculate the funds for the whole chama
	funds = calculateChamaFunds(session_chamaID)

	form = forms.addTransaction(session_chamaID)

	context = {'form': form}
	if request.method == 'POST':

		#check if the amount is valid
		if int(request.POST.get('amount')) < 1:
			messages.warning(request, "Amount must be greater than 0")
			return HttpResponseRedirect('transactionsform')

		#check if the amount exceeds available funds for withdrawals
		if (request.POST.get('transactionType') == 'withdrawal' and funds - int(request.POST.get('amount'))) < 0:
			messages.warning(request, "Not enough funds to give %s" % request.POST.get('amount'))
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
	paginated_members = Paginator(members_list, 10)
	page_number = request.GET.get('page')
	page_object= paginated_members.get_page(page_number)

	context = {'page_object': page_object}

	return render(request, 'dashboard/chamaMembers.html', context)

#Member deletion view
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def deleteUser(request, chamaID = None, username = None):
	session_chamaID = request.user.chamas.chamaID

	#declare context
	context = {}

	#to prevent admins from deleting the group
	if request.user.username == username:
		messages.warning(request, "Call 0798380239 to change the group admin. Note: Changing admin will cost KSH30")
		return HttpResponseRedirect('/members')

	#to ensure a chama admin can disable only their members
	if session_chamaID == chamaID:
		#Get the username of member to be deleted
		user = User.objects.get(username = username)
		context = {'prompt': "Delete %s" %user.first_name}

		if request.method == "POST":
			confirmation = request.POST.get('confirmation')

			if confirmation == "yes":
				user.is_active = False
				user.save()
				messages.success(request, user.first_name + ' has been removed from ' + request.user.chamas.chamaName)
			elif confirmation == "no":
				messages.warning(request, 'deletion of %s cancelled' %user.first_name)
			else:
				messages.warning(request, 'invalid input')

			return HttpResponseRedirect('/members')
	else:
		messages.warning(request, 'The member does not exist')
		return HttpResponseRedirect('/members')

	return render(request, 'dashboard/deleteUser.html', context)

#This view displays all transactions of the authenticated chama
@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def transactions(request):
	session_chamaID = request.user.chamas.chamaID
	transactions = Transactions.objects.filter(memberID__chamaID = session_chamaID).order_by("-transactionDate")
	paginated_transactions = Paginator(transactions, 10)
	page_number = request.GET.get('page')
	page_object= paginated_transactions.get_page(page_number)

	context = {'page_object': page_object, 'transactions': transactions}

	return render(request, 'dashboard/transactions.html', context)

@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_admin'])
def loans(request):
	session_chamaID = request.user.chamas.chamaID
	loanSettings = LoanSettings.objects.get(chamaID = session_chamaID)
	loanForm = forms.loanForm(session_chamaID)	
	context = {'loanSettings': loanSettings, 'loanForm': loanForm}

	funds = calculateChamaFunds(session_chamaID)

	if request.method == "POST":
		if "submit_loan_settings" in request.POST:
			loanSettings.interestRate = request.POST.get('interest_rate')
			loanSettings.repaymentPeriod = request.POST.get('repayment_period')
			loanSettings.save()
			messages.success(request, "Loan settings changed")

		elif "submit_loan" in request.POST:
			loanForm = forms.loanForm(session_chamaID, data = request.POST)
			#check if chama has enough money
			amount = int(request.POST.get('amount'))
			if(funds - amount) < 0:
				messages.warning(request, "There is no enough money to issue %d" %amount)

			else:
				if loanForm.is_valid():
					loanFormInstance = loanForm.save(commit = False)
					loanFormInstance.repaymentAmount = loanFormInstance.amount + ((loanSettings.interestRate/100)*loanFormInstance.amount)
					loanFormInstance.repaymentDate = loanFormInstance.issueDate + timezone.timedelta(days = loanSettings.repaymentPeriod)
					loanFormInstance.save()
					messages.success(request, "Loan issued")
				else:
					messages.warning(request, "something went wrong")
		else:
			#meme this person if they are making a bad request
			return HttpResponseRedirect('https://bit.ly/3lZ8kiV')

	return render(request, 'dashboard/loans.html', context)


@login_required(login_url = 'login')
@userAuthenticated(allowed_roles = ['chama_member', 'chama_admin'])
def loansPage(request):
	session_chamaID = request.user.chamas.chamaID
	loans = Loans.objects.filter(memberID__chamaID = session_chamaID).order_by("-issueDate")
	context = {'loans': loans}

	return render(request, 'dashboard/loansPage.html', context)

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
		paginated_transactions = Paginator(transactions, 10)
		page_number = request.GET.get('page')
		page_object= paginated_transactions.get_page(page_number)
		numberOfTransactions = Transactions.objects.filter(memberID = userInfo).count()
		funds = calculateMemberFunds(userInfo);

		context = {"viewingUser":viewingUser, "userInfo": userInfo, "userGroup": userGroup, "funds": funds, "numberOfTransactions" :numberOfTransactions, 'page_object':page_object}
	
	else:
		return HttpResponse('You are not authorized to view this page')

	return render(request, 'dashboard/memberPage.html', context)