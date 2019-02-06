
""" -- Django Libraries -- """
from django.conf.urls import url

""" --  Project Libraries -- """
from MyApp import views

urlpatterns = [
    url(r'^transaction/(?P<id>\w+)', views.getTransaction),
    url(r'^transactionSummaryByProducts/(?P<days>\w+)', views.getTransactionSummaryByProducts),
    url(r'^transactionSummaryByManufacturingCity/(?P<days>\w+)', views.getTransactionSummaryByManufacturingCity),
]