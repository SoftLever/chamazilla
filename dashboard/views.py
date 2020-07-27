from django.shortcuts import render, redirect
from .models import ChamaMembers, Transactions, Chamas
from . import forms

def dashboard(request):
	transactions = Transactions.objects.all().order_by("-transactionDate")[:5]
	members_count = ChamaMembers.objects.filter(chamaID = "CSG00004").count()
	chamaInfo = Chamas.objects.filter(chamaID = 'CSG00004').last()

	return render(request, 'dashboard.html', {'transactions': transactions, 'chamaInfo': chamaInfo, 'members_count': members_count})

def members(request):
	form = forms.CreateUser()
	members_list = ChamaMembers.objects.filter(chamaID = "CSG00004")
	if request.method == 'POST':
		form = forms.CreateUser(request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			#instance.chamaID = "CSG00004"
			instance.save()
			print("New member added")
			#redirect('reports.html')

	return render(request, 'chamaMembers.html', {'form': form, 'members_list': members_list})

def transactions(request):
	form = forms.addTransaction()
	transactions = Transactions.objects.all().order_by("-transactionDate")
	if request.method == 'POST':
		form = forms.addTransaction(request.POST)
		if form.is_valid():
			instance = form.save(commit = False)
			print(instance.amount)

			#update the total funds of the chama
			chamaInfo = Chamas.objects.filter(chamaID = 'CSG00004').last()
			chamaInfo.funds += instance.amount
			instance.save()
			chamaInfo.save()
			print("New Transaction recorded, funds updated")

	return render(request, 'transactions.html', {'form': form, 'transactions': transactions})

def loans(request):
	return render(request, 'loans.html')