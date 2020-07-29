from django.shortcuts import render

def index(request):
	return render(request, 'member_records/index.html')

def signup(request):
	return render(request, 'member_records/signup.html')