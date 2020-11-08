from django.urls import path, include
from django.conf.urls import re_path
from .views import api_views

#For generation of tokens to views
from rest_framework.authtoken import views

#The REST Framework router will make sure our requests end up at the right resource dynamically
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'transactions', api_views.TransactionsViewSet, basename = 'Transactions')
router.register(r'members', api_views.MembersViewSet, basename = 'Members')
router.register(r'subscription', api_views.SubscriptionViewSet, basename = 'Subscriptions')
router.register(r'loansettings', api_views.LoanSettingsViewSet, basename = 'LoanSettings')
router.register(r'loans', api_views.LoansViewSet, basename = 'Loans')


urlpatterns = [
	re_path(r'', include(router.urls)),
    re_path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'^getapitoken$', views.obtain_auth_token),
]