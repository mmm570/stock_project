from django.urls import path
from choose import views

app_name='choose'
urlpatterns=[
    path('',views.choose, name='choose'),
    path('timely_stock',views.timely_stock, name='timely_stock'),
    path('choose2',views.choose2, name='choose2'),
    path('choose2_submit',views.choose2_submit, name='choose2_submit'),
    #path('addrandom',views.addrandom, name='addrandom'),
    #path('random',views.random, name='random'),
    ] 