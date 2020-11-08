from rest_framework import viewsets
from rest_framework.response import Response
from ..serializers import TransactionSerializer, ChamaMemberSerializer, SubscriptionSerializer, LoanSettingSerializer, LoanSerializer
from ..models import Transactions, ChamaMembers, Subscriptions, LoanSettings, Loans

#To handle relationships that involve users
from django.contrib.auth.models import User

#To restrict viewing of info to authenticated users
from rest_framework.permissions import IsAuthenticated

class TransactionsViewSet(viewsets.ViewSet):

	def list(self, request):
		chamaid = request.user.chamas.chamaID
		queryset = Transactions.objects.filter(memberID__chamaID = chamaid).order_by("-transactionDate")
		serializer = TransactionSerializer(queryset, many = True)
		return Response(serializer.data)


class MembersViewSet(viewsets.ViewSet):

	def list(self, request):
		chamaid = request.user.chamas.chamaID
		queryset = ChamaMembers.objects.filter(chamaID = chamaid, user__is_active = True).order_by("-memberID")
		serializer = ChamaMemberSerializer(queryset, many = True)
		return Response(serializer.data)

class SubscriptionViewSet(viewsets.ModelViewSet):

	def list(self, request):
		chamaid = request.user.chamas.chamaID
		queryset = Subscriptions.objects.filter(chamaID = chamaid)
		serializer = SubscriptionSerializer(queryset, many = True)
		return Response(serializer.data)

class LoanSettingsViewSet(viewsets.ModelViewSet):

	def list(self, request):
		chamaid = request.user.chamas.chamaID
		queryset = LoanSettings.objects.get(chamaID = chamaid)
		serializer = LoanSettingSerializer(queryset, many = False)
		return Response(serializer.data)

class LoansViewSet(viewsets.ModelViewSet):
	def list(self, request):
		chamaid = request.user.chamas.chamaID
		queryset = Loans.objects.filter(memberID__chamaID = chamaid).order_by("-issueDate")
		serializer = LoanSerializer(queryset, many = True)
		return Response(serializer.data)