from django.contrib import admin
from django.urls import path, include
from django.conf.urls import re_path
from member_records.views import index, api, signup, loginpage, logoutUser
from dashboard.views.views import dashboard, members, transactions, loans, membersform, transactionsform, memberPage, deleteUser, loansPage

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', index, name = "index"),
    re_path(r'^api$', api, name = "api"),
    re_path(r'^signup$', signup, name = "signup"),
    re_path(r'^login$', loginpage, name = "login"),
    re_path(r'^logout$', logoutUser, name = "logout"),
    re_path(r'^dashboard/$', dashboard, name = "dashboard"),
    re_path(r'^members$', members, name = "members"),
    re_path(r'^membersform$', membersform, name = "membersform"),
    re_path(r'^transactions$', transactions, name = "transactions"),
    re_path(r'^transactionsform$', transactionsform, name = "transactionsform"),
    re_path(r'^loans$', loans, name = "loans"),
    re_path(r'^loanspage', loansPage, name = "loanspage"),
    re_path(r'^memberpage/(?P<username>[0-9]+)/$', memberPage, name = "memberpage"),
    re_path(r'^delete/(?P<chamaID>\w+)/(?P<username>[0-9]+)/$', deleteUser, name = "delete"),
    re_path(r'^restapi/', include('dashboard.api_urls')),
]