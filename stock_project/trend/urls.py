from django.urls import path
from trend import views

app_name='trend'
urlpatterns=[
    path('',views.trend, name='trend'),
    # path('trend_stock',views.trend_stock, name='trend_stock'),
    path('addtrend',views.addtrend, name='addtrend'),
    path('trend2',views.trend2, name='trend2'),
    ] 