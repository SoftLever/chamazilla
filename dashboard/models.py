from django.db import models
from django.contrib.auth.models import User

#for fields that have a default datetime
from django.utils import timezone

#for the transactionid field
import datetime

#for validation of amount
from django.core.validators import MinValueValidator

#This is a table that holds only 4 records - The numbers that will help in assigning IDs
#fields names are fixed, they should NEVER BE EDITED
#currentNumber should not be edited manually
#the field names are; 'transactionid, chamaid, memberid', 'subscriptionid'
class fieldID(models.Model):
	fieldName = models.CharField(primary_key = True, max_length = 20)
	currentNumber = models.IntegerField(default = 0)

	def __str__(self):
		return self.fieldName

#Functions that assign chamaID, memberID, subscriptionID and transactionID
def getNextID(fieldName):
	lastID = fieldID.objects.filter(fieldName = fieldName).last()
	lastID.currentNumber +=1
	lastID.save()
	nextID = lastID.currentNumber

	print(nextID)

	return nextID

def generate_ChamaID():
	nextID = getNextID("chamaid")
	chamaID = "CZG" + str(nextID).zfill(5)
	
	print(chamaID)

	return chamaID

def generate_TransactionID():
	nextID = getNextID("transactionid")
	transactionID = "CZT" + str(nextID).zfill(10) + datetime.date.today().strftime("%y")

	print(transactionID)

	return transactionID

def generate_memberID():
	nextID = getNextID("memberid")
	memberID = "CZM" + str(nextID).zfill(10)

	print(memberID)

	return memberID

def generate_SubscriptionID():
	nextID = getNextID("subscriptionid")
	subscriptionID = "CZS" + str(nextID).zfill(10)

	print(subscriptionID)

	return subscriptionID

def generate_loanID():
	nextID = getNextID("loanid")
	loanID = "CZL" + str(nextID).zfill(10)

	return loanID

#A one column table that stores transaction types only
#transaction types; merry-go-round, savings, development, fine
class TransactionTypes(models.Model):
	transactionType = models.CharField(primary_key = True, max_length = 30)

	def __str__(self):
		return self.transactionType

#CSM, CSG, CST stand for Chama Smart Member, Group and Transaction successfully

class Chamas(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	chamaID = models.CharField(primary_key = True, max_length = 15, default = generate_ChamaID)#add default value
	chamaName = models.CharField(max_length = 50)
	regDate = models.DateTimeField(default = timezone.now)
	
	def __str__(self):
		return self.chamaID

class ChamaMembers(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	memberID = models.CharField(primary_key = True, max_length = 15, default = generate_memberID)
	chamaID = models.ForeignKey(Chamas, on_delete = models.CASCADE)
	
	def __str__(self):
		return self.user.first_name + ' ' + self.user.last_name

class Transactions(models.Model):
	transactionID = models.CharField(primary_key = True, max_length = 20, default = generate_TransactionID)
	transactionType = models.ForeignKey(TransactionTypes, on_delete = models.CASCADE)
	memberID = models.ForeignKey(ChamaMembers, on_delete = models.CASCADE)
	transactionDate = models.DateTimeField(default = timezone.now)
	amount = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.transactionID

#This one-column table will have fixed records
#subscription types: paid, trial
class SubscriptionTypes(models.Model):
	subscriptionType = models.CharField(primary_key = True, max_length = 10)

	def __str__(self):
		return self.subscriptionType

#This function will add 7 days to the current time
def set_Transaction_Expiry():
	return timezone.now() + timezone.timedelta(days = 14)

#This will be manually edited from the admin site when a chama pays for subscription
class Subscriptions(models.Model):
	subscriptionID = models.CharField(primary_key = True, max_length = 20, default = generate_SubscriptionID)
	subscriptionType = models.ForeignKey(SubscriptionTypes, default = "trial", on_delete = models.CASCADE)
	chamaID = models.ForeignKey(Chamas, on_delete = models.CASCADE)
	startDate = models.DateTimeField(default = timezone.now)
	endDate = models.DateTimeField(default = set_Transaction_Expiry)
	amount = models.IntegerField(default = 0)

	def __str__(self):
		return self.subscriptionID

def set_Repayment_Date():
	return timezone.now() + timezone.timedelta(days = 30)

class LoanStatus(models.Model):
	loanStatusID = models.CharField(primary_key = True, max_length = 10)

	def __str__(self):
		return self.loanStatusID

class LoanSettings(models.Model):
	chamaID = models.OneToOneField(Chamas, primary_key = True, on_delete = models.CASCADE)
	interestRate = models.DecimalField(default = 10.00, max_digits = 5, decimal_places = 2)
	repaymentPeriod = models.IntegerField(default = 30)

	#def __str__(self):
	#	return self.chamaID

class Loans(models.Model):
	loanID = models.CharField(primary_key = True, max_length = 30, default = generate_loanID)
	memberID = models.ForeignKey(ChamaMembers, on_delete = models.CASCADE)
	amount = models.IntegerField(default = 0)
	repaymentAmount = models.IntegerField(default = amount)
	issueDate = models.DateTimeField(default = timezone.now)
	repaymentDate = models.DateTimeField(default = set_Repayment_Date)
	status = models.ForeignKey(LoanStatus, on_delete = models.CASCADE, default = "unpaid")

	def __str__(self):
		return self.loanID