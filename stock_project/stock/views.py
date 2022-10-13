from django.shortcuts import render
import requests
from bs4 import BeautifulSoup

def stock(request):
    url='https://tw.stock.yahoo.com/tw-market'
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    d=[]
    i=0
    f=0
    for a in soup.find_all('h3',{'class':'Mt(0) Mb(8px)'}):
        d.append([a.text,a.a.get('href')])
        i+=1
        if i == 10:
            break
    for b in soup.find_all('p',{'class':'Fz(16px) Lh(24px) LineClamp(2,48px) C($c-secondary-text) M(0)'}):
        d[f].append(b.text)
        f+=1
        if f == 10:
            break
    return render(request,'stock/homepage.html',{'d':d})