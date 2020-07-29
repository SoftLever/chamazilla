from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from member_records.views import index, signup
from dashboard.views import dashboard, members, transactions, loans, membersform, transactionsform

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index, name = "index"),
    url(r'^signup$', signup, name = "signup"),
    url(r'^dashboard/$', dashboard, name = "dashboard"),
    url(r'^members$', members, name = "members"),
    url(r'^membersform$', membersform, name = "membersform"),
    url(r'^transactions$', transactions, name = "transactions"),
    url(r'^transactionsform$', transactionsform, name = "transactionsform"),
    url(r'^loans$', loans, name = "loans"),
]