from rest_framework import serializers

from .models import Transactions, ChamaMembers, Subscriptions, LoanSettings, Loans

class ChamaMemberSerializer(serializers.ModelSerializer):
	class Meta:
		model = ChamaMembers
		fields = ['memberID', 'user']

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transactions
		fields = ['transactionID', 'transactionType', 'memberID', 'transactionDate', 'amount']

class SubscriptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Subscriptions
		fields = ['subscriptionID', 'subscriptionType', 'startDate', 'endDate', 'amount']

class LoanSettingSerializer(serializers.ModelSerializer):
	class Meta:
		model = LoanSettings
		fields = ['interestRate', 'repaymentPeriod']

class LoanSerializer(serializers.ModelSerializer):
	class Meta:
		model = Loans
		fields = ['loanID', 'memberID', 'amount', 'repaymentAmount', 'issueDate', 'repaymentDate', 'status']