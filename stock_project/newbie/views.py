from django.shortcuts import render

def newbie(request):
    return render(request,'newbie/newbie.html')