"""stock_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from stock import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/',include('stock.urls',namespace='stock')),
    path('markettrend/',include('markettrend.urls',namespace='markettrend')),
    path('choose/',include('choose.urls',namespace='choose')),
    path('chips/',include('chips.urls',namespace='chips')),
    path('trend/',include('trend.urls',namespace='trend')),
    path('newbie/',include('newbie.urls',namespace='newbie')),
    path('transaction/',include('transaction.urls',namespace='transaction')),
    path('predict/',include('predict.urls',namespace='predict')),
    re_path('.*',views.stock),
    ]
