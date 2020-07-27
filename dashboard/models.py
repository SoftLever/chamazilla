from django.db import models
import datetime

#This is a table that holds only 3 records - The numbers that will help in assigning IDs
#fields names are fixed, they should NEVER BE EDITED
#currentNumber should not be edited manually
#the field names are; 'transactionid, chamaid, memberid'
class fieldID(models.Model):
	fieldName = models.CharField(primary_key = True, max_length = 13)
	currentNumber = models.IntegerField(default = 0)

	def __str__(self):
		return self.fieldName

#Functions that assign chamaID, memberID, and transactionID
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

#A one column table that stores transaction types only
class TransactionTypes(models.Model):
	transactionType = models.CharField(primary_key = True, max_length = 30)

	def __str__(self):
		return self.transactionType

#CSM, CSG, CST stand for Chama Smart Member, Group and Transaction successfully

class Chamas(models.Model):
	chamaID = models.CharField(primary_key = True, max_length = 15, default = generate_ChamaID)#add default value
	chamaName = models.CharField(max_length = 50)
	#add repID here
	subscription = models.CharField(max_length = 5)#trial, paid, default trial
	regDate = models.DateTimeField(auto_now_add = True)
	funds = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.chamaID

class ChamaMembers(models.Model):
	memberID = models.CharField(primary_key = True, max_length = 15, default = generate_memberID)
	firstName = models.CharField(max_length = 30)
	secondName = models.CharField(max_length = 30)
	chamaID = models.ForeignKey(Chamas, on_delete = models.CASCADE)
	status = models.CharField(max_length = 8)#active, removed, default value of active
	
	def __str__(self):
		return self.memberID

class Transactions(models.Model):
	transactionID = models.CharField(primary_key = True, max_length = 20, default = generate_TransactionID)
	transactionType = models.ForeignKey(TransactionTypes, on_delete = models.CASCADE)
	memberID = models.ForeignKey(ChamaMembers, on_delete = models.CASCADE)
	transactionDate = models.DateTimeField(auto_now_add = True)
	amount = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.transactionID