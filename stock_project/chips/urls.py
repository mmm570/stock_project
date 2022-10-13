from django.urls import path
from chips import views

app_name='chips'
urlpatterns=[
    path('',views.chips, name='chips'),
    path('chips2',views.chips2, name='chips2'),
    ] 
