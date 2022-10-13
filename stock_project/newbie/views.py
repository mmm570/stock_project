from django.shortcuts import render
from django.template.context_processors import request
from django.http.response import HttpResponse

def newbie(request):
    return render(request,'newbie/newbie.html')