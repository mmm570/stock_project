from django.urls import path
from transaction import views

app_name='transaction'
urlpatterns = [
    path('', views.transaction, name='transaction'),
    path('login_register/', views.login_register,name='login_register'),
    path('btn1Create/', views.btn1Create,name='btn1Create'),
    path('btn2Create/', views.btn2Create,name='btn2Create'),
    path('btn3Create', views.btn3Create,name='btn3Create'),
    path('btn4Create/', views.btn4Create,name='btn4Create'),
    path('btn5Create/', views.btn5Create,name='btn5Create'),
    path('btn1Create/clickbuy1', views.clickbuy1,name='clickbuy1'),
    path('btn1Create/buy_sell', views.buy_sell,name='buy_sell'),
    path('logout', views.logout,name='logout'),
]

