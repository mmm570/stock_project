from django.urls import path
from markettrend import views

app_name='markettrend'
urlpatterns=[
    path('',views.markettrend, name='markettrend'),
    ] 