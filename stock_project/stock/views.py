from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.offline as opy
from urllib.parse import quote

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
    
    #大盤
    dtime = int(float(time.time())*1000)
    url = 'https://mis.twse.com.tw/stock/data/mis_ohlc_TSE.txt?_='+str(dtime)
    res = requests.get(url)
    jd = res.json()['ohlcArray']
    columns = ['c','s','ts','t']
    df = pd.DataFrame(jd, columns=columns)
    df.columns =['加權指數','成交金額','時間','日期']
    df['加權指數'] = pd.to_numeric(df['加權指數'])
    df['成交金額'] = df['成交金額'].astype(float)
    df['時間']=df['時間'].replace(np.nan,'133000')
    yesterday =res.json()['infoArray']
    df2=pd.DataFrame([yesterday[0]['y'], 0 , '0900' ,np.nan]).T
    #df.loc[0]=[yesterday[0]['y'], 0 , '0900' ,np.nan]
    df2.columns =df.columns
    df=pd.concat([df2,df],axis=0,ignore_index=True)
    allMoney=0
    for i in range(len(df['加權指數'])):#注意
            df['時間'][i]=df['時間'][i][0:2]+':'+df['時間'][i][2:4] 
            df['成交金額'][i]=df['成交金額'][i]/100 
            allMoney+=df['成交金額'][i]
            allMoney=round(allMoney,2)
    abc=str(df['加權指數'][len(df['加權指數'])-1])
    df['昨收價']=df['加權指數'][0]
    trace1 = go.Bar(
        name='成交金額(億)',
        x=df['時間'],
        y=df['成交金額'],
    
    )
    trace2 = go.Scatter(
        name='加權指數',
        x=df['時間'],
        y=df['加權指數'],
        yaxis="y2",
    )
    trace3 = go.Scatter(
        name='昨收',
        x=df['時間'],
        y=df['昨收價'],
        yaxis="y2",
    )
    
    data = [trace1,trace2,trace3]
    layout = go.Layout(
        yaxis=dict(
            domain=[0, 0.7]
        ),
        yaxis2=dict(
            domain=[0.7, 1]
        ),
        title='加權指數:'+abc,
    )
    fig =go.Figure(data=data, layout=layout)
    fig.update_xaxes(tick0='0900',dtick=5)
    fig.update_yaxes(exponentformat="none")
    fig.update_layout(hovermode="x unified",height=500)
#    fig.add_shape(type="line",
#        x0=str(df.index[0]), y0=df['加權指數'][0], x1=str(df.index[-1]), y1=df['加權指數'][0],
#        line=dict(color="gray",width=1)
#    )
    div = opy.plot(fig, auto_open=False, output_type='div')
    
    
    
     # 要抓取的網址
    url='https://tw.stock.yahoo.com/rank/price?exchange=TAI'
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    stock = []
    
    
    i=0
    for a in soup.find_all('div',{'class':'Bgc(#fff) table-row D(f) Ai(c) Bgc(#e7f3ff):h Fz(16px) Px(12px) Bxz(bb) Bdbs(s) Bdbw(1px) Bdbc($bd-primary-divider) H(52px) H(a)--mobile'}):
        a1=a.find('div',{'class':'Lh(20px) Fw(600) Fz(16px) Ell'})
        a2=a.find('div',{'class':'D(f) Ai(c)'})
        stock.append([a1.text+a2.text])#股票名稱
        
        a3=a.find('div',{'class':'Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(76px)'})
        stock[i].append(a3.text)#股票價格
        
        a4=a.find('span',{'class':'Mend(4px) Bds(s)'})
        k=''
        if a4==None:
            k=''
        elif a4.get('style') == "border-color:transparent transparent #ff333a transparent;border-width:0 5px 7px 5px": 
            k='+'
        else:
            k='-'
        a5=a.find('span',{'class':'Fw(600) Jc(fe) D(f) Ai(c) C($c-trend-up)'})#漲跌
        j=0
        if a5==None:
            a5=a.find('span',{'class':'Fw(600) Jc(fe) D(f) Ai(c) C($c-trend-down)'})
            if a5==None:
                j=1
        a5=str(a5) #轉字串
        a55=a5.find('</span>')#抓索引直
        if j==0:
            stock[i].append(k+a5[a55+7:-7])#股票漲跌 
        else:
            stock[i].append('0')
        
        
        
        #漲跌幅
        a6=a.find_all('div',{'class':'Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(76px)'},limit=3)
        chinese=str(a6[2])
        index=chinese.find('</span>')
        if chinese[index+7:-13]=="":
            stock[i].append('0%')
        else:
            stock[i].append(k+chinese[index+7:-13])#股票漲跌幅度%
        
            
            
        a7=a.find('div',{'class':'Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(80px)'})
        stock[i].append(a7.text)#成交量(張)
        
        
        a8=a.find('div',{'class':'Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend(0):lc Miw(88px) Mend(12px)'})
        stock[i].append(a8.text)#成交金額(億)
        
        
        
        i+=1
        if i == 5: #抓前十筆
            break
            

    efg=float(abc)-float(df['加權指數'][0])
    hij=str(round((efg/float(abc)*100),2))
    stock_data=[]
    stock_data_2=[]
    stock_data.append(abc)
    stock_data.append('%.2f' %efg)
    stock_data.append(hij)
    stock_data_2.append(allMoney)
    return render(request,'stock/homepage.html',{'d':d,'fig':div,'stock_data':stock_data,'stock_data_2':stock_data_2,'stock':stock})