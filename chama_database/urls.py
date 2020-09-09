from django.contrib import admin
from django.urls import path
from django.conf.urls import url, re_path
from member_records.views import index, signup, loginpage, logoutUser
from dashboard.views import dashboard, members, transactions, loans, membersform, transactionsform, memberPage, deleteUser, loansPage

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index, name = "index"),
    url(r'^signup$', signup, name = "signup"),
    url(r'^login$', loginpage, name = "login"),
    url(r'^logout$', logoutUser, name = "logout"),
    url(r'^dashboard/$', dashboard, name = "dashboard"),
    url(r'^members$', members, name = "members"),
    url(r'^membersform$', membersform, name = "membersform"),
    url(r'^transactions$', transactions, name = "transactions"),
    url(r'^transactionsform$', transactionsform, name = "transactionsform"),
    url(r'^loans$', loans, name = "loans"),
    re_path(r'^loanspage', loansPage, name = "loanspage"),
    url(r'^memberpage/(?P<username>[0-9]+)/$', memberPage, name = "memberpage"),
    url(r'^delete/(?P<chamaID>\w+)/(?P<username>[0-9]+)/$', deleteUser, name = "delete"),
]