from django.db import models
from django.contrib.auth.models import User
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
	chamaID = "CSG" + str(nextID).zfill(5)
	
	print(chamaID)

	return chamaID

def generate_TransactionID():
	nextID = getNextID("transactionid")
	transactionID = "CST" + str(nextID).zfill(10) + datetime.date.today().strftime("%y")

	print(transactionID)

	return transactionID

def generate_memberID():
	nextID = getNextID("memberid")
	memberID = "CSM" + str(nextID).zfill(10)

	print(memberID)

	return memberID

def generate_SubscriptionID():
	nextID = getNextID("subscriptionid")
	subscriptionID = "CSS" + str(nextID).zfill(10)

	print(subscriptionID)

	return subscriptionID

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
	#add repID here
	regDate = models.DateTimeField(auto_now_add = True)
	
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
	transactionDate = models.DateTimeField(auto_now_add = True)
	amount = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.transactionID

#This one-column table will have fixed records
#subscription types: paid, trial
class SubscriptionTypes(models.Model):
	subscriptionType = models.CharField(primary_key = True, max_length = 10)

	def __str__(self):
		return self.subscriptionType

#This will be manually edited from the admin site when a chama pays for subscription
class Subscriptions(models.Model):
	subscriptionID = models.CharField(primary_key = True, max_length = 20, default = generate_SubscriptionID)
	subscriptionType = models.ForeignKey(SubscriptionTypes, default = "trial", on_delete = models.CASCADE)
	chamaID = models.ForeignKey(Chamas, on_delete = models.CASCADE)
	startDate = models.DateTimeField(auto_now_add = True)
	endDate = models.DateTimeField(default = datetime.datetime.now() + datetime.timedelta(7))
	amount = models.IntegerField(default = 0)

	def __str__(self):
		return self.subscriptionID