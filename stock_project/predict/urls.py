from django.urls import path
from predict import views

app_name='predict'
urlpatterns=[
    path('',views.predict, name='predict'),
    path('newUrl',views.newUrl, name='newUrl'),
    path('newImg',views.newImg, name='newImg'),
    ] 