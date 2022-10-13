from django.urls import path
from newbie import views

app_name='newbie'
urlpatterns=[
    path('',views.newbie, name='newbie'),
    ] 