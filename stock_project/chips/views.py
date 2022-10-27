from django.shortcuts import render
import pandas
from chips.forms import chips_form

def chips(request):
    df = pandas.read_html('https://histock.tw/stock/rank.aspx?m=0&d=0&p=all') #m=列，d=排序方式(0-小到大，1-大到小)
    df[0].columns=['代號','名稱','價格','漲跌','漲跌幅','周漲跌','振幅','開盤','最高','最低','昨收','成交量','成交值(億)']
    ab=df[0]
    #for i in range(len(ab)):
    ab['漲跌']=ab['漲跌'].str.replace('▲','+')
    ab['漲跌']=ab['漲跌'].str.replace('▼','')
    div='<div>'+ab.to_html(index=False)+'</div>' 
    title='代號:由大到小排序'
    return render(request,'chips/chips.html',{'who':chips_form(),'table':div,'title':title})
def chips2(request): #開盤沒有排序
    M_text=request.GET['table1']
    D_text=request.GET['table2']
    if M_text == "0":
        title="代號"
    elif M_text == "1":
        title="名稱"
    elif M_text == "2":
        title="價格"
    elif M_text == "3":
        title="漲跌"
    elif M_text == "4":
        title="漲跌幅"
    elif M_text == "6":
        title="周漲跌"
    elif M_text == "7":
        title="振幅"
    elif M_text == "8":
        title="最高"
    elif M_text == "9":
        title="最低"
    elif M_text == "10":
        title="昨收"
    elif M_text == "11":
        title="成交量"
    elif M_text == "13":
        title="成交值(億)"
       
    if D_text == "0":
        title+=':由小到大排序'
    else:
        title+=':由大到小排序'
    df = pandas.read_html('https://histock.tw/stock/rank.aspx?m='+M_text+'&d='+D_text+'&p=all') #m=列，d=排序方式(0-小到大，1-大到小)
    df[0].columns=['代號','名稱','價格','漲跌','漲跌幅','周漲跌','振幅','開盤','最高','最低','昨收','成交量','成交值(億)']
    ab=df[0]
    #for i in range(len(ab)):
    ab['漲跌']=ab['漲跌'].str.replace('▲','+')
    ab['漲跌']=ab['漲跌'].str.replace('▼','')
    ab['昨收']=ab['昨收'].round(2)

    div='<div  id="chips_div">'+ab.to_html(index=False)+'</div>'   
    return render(request,'chips/chips.html',{'who':chips_form(),'title':title,'table':div})

