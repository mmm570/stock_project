from django.shortcuts import render,redirect
from django.template.context_processors import request
from django.http.response import HttpResponse
from transformers import BertTokenizer, TFBertForSequenceClassification
from transformers import InputExample, InputFeatures
import tensorflow as tf
import os
import requests
import pandas as pd 
from urllib.parse import quote
import time
#下載新聞標題及內容到電腦磁碟
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import numpy as np
from predict.forms import new_forms, new_Imgforms
from django.contrib import messages 
import plotly.graph_objects as go  
import plotly.offline as opy
import json

import yfinance as yf
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from dateutil.relativedelta import relativedelta
import sklearn.metrics as metrics

def predict(request):
    return render(request,'predict/predict.html',{'who':new_forms(),'who2':new_Imgforms()})
def newUrl(request):
    try:
        stock_new_url = request.GET.get("url")
        output_dir = './model_save1/'
        
        
        os.chdir(r'C:\Users\sleep\Desktop') 
        
        model =TFBertForSequenceClassification.from_pretrained(output_dir )
        tokenizer = BertTokenizer.from_pretrained(output_dir)
        
        #stock_new_url='https://tw.stock.yahoo.com/news/%E5%8F%B0%E7%A9%8D%E9%9B%BB%E6%A5%A0%E6%A2%93%E7%94%A2%E6%A5%AD%E5%9C%92%E5%8B%95%E5%9C%9F-%E5%91%A8%E9%82%8A%E6%88%BF%E5%B8%82%E6%9C%80%E9%AB%98%E6%BC%B2%E9%80%BE-3-%E6%88%90-040857735.html'
        response = requests.get(stock_new_url)
        soup = BeautifulSoup(response.text, "html.parser")         
        
        b=0
        newData=[]
        h1=soup.find('h1')
        content= soup.find('div',{'class':'caas-body'}) 
        time=soup.find('time',{'class':'caas-attr-meta-time'})
        newData.append([h1.text,time.text,content.text])
    
    
    
        pre_text= [newData[0][2]]
        tf_batch = tokenizer(pre_text[0][11:], max_length=128, padding=True, truncation=True, return_tensors='tf')
        tf_outputs = model(tf_batch)
        tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
        labels = ['非常好','好','普通','不好','非常不好']  #好到壞
        label = tf.argmax(tf_predictions, axis=1)
        label = label.numpy()
        newData[0].append(labels[label[0]])
    except:
        messages.success(request,'錯誤網址')
        return redirect('predict:predict')
    return render(request, 'predict/predict_news.html',{'newData':newData})  
def newImg(request):
    
    output_dir = './model_save1/'

    os.chdir(r'C:\Users\sleep\Desktop') 
    
    model =TFBertForSequenceClassification.from_pretrained(output_dir )
    tokenizer = BertTokenizer.from_pretrained(output_dir)
    
    #print(df[0])
    get_text= request.GET.get("code")
    stock=[]
    with open('test3.json',encoding="utf_8") as f:
            data = json.load(f)
    for i in range(len(data)-1):
        if get_text == data[i]['name']:
            targets=data[i]['stock']
            stock.append(targets)
            stock.append(get_text)
        elif get_text ==data[i]['stock']:
            targets=get_text
            stock_name=data[i]['name']
            stock.append(targets)
            stock.append(stock_name)
        #主程式主程式主程式主程式主程式主程式主程式主程式主程式主程式主程式主程式主程式主程式
         # 要抓取的網址
    storestock=['2610','2330','2618','2303','2609']
    if targets in storestock:
        f = open(r'C:/Users/sleep/Desktop/'+targets+'.txt', encoding='UTF-8') #開新聞黨
        date1 = [] #日期
        pre = []  #預測後解果
        for line in f.readlines():
            tf_batch = tokenizer(line[11:], max_length=128, padding=True, truncation=True, return_tensors='tf')
            tf_outputs = model(tf_batch)
            tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
            labels = ['5','4','3','2','1']    #好到壞
            label = tf.argmax(tf_predictions, axis=1)
            label = label.numpy()
            for i in range(len(line)):
                pre.append(labels[label[i]])  #儲存
                date1.append(line[0:10])    #儲存
                break
        f.close
    else:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        url="https://tw.stock.yahoo.com/quote/"+targets+"/news"
        #print(url)
        
          #請求網站
        list_req = requests.get(url, headers=headers)
          #將整個網站的程式碼爬下來
        soup = BeautifulSoup(list_req.content, "html.parser")
          #找到b這個標籤
            
        now =time.localtime()  #當日時間
        now = str(now.tm_year)+'年'+str(now.tm_mon)+'月'+ str(now.tm_mday)+'日' 
        num=now.find('日')
        
                    
        driver = webdriver.Chrome(r"C:\Users\sleep\Desktop\newgit\newstock\stock_project\predict\chromedriver")#options=options
        
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
          "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
        })
        
        
        driver.get("https://tw.stock.yahoo.com/quote/"+targets+"/news")
        time.sleep(3)
        driver.refresh()
        time.sleep(2)
        for x in range(1, 3):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
        soup = BeautifulSoup(driver.page_source,'lxml')
        NewData=[]
        stock_name=stock[1]
        for a in soup.find_all('h3',{'class':'Mt(0) Mb(8px)'}):
            if stock_name in a.text:
                #print(a.a.get('href'))
                #print(a.text)
                url = a.a.get('href')
                list_req = requests.get(url)
                soup1 = BeautifulSoup(list_req.content, "html.parser")
                getAllNew= soup1.find('div',{'class':'caas-body'}) 
                gettime= soup1.find('time',{'class':'caas-attr-meta-time'}) #抓日期
                #print(getAllNew.text+'\n')
                #f.write(a.text+'\n')             #標題
                NewData.append([gettime.get_text('datetime')[0:10],getAllNew.text])
        #print(NewData)      
        
        date1 = [] #日期
        pre = []  #預測後解果
    
        for line in NewData:
            tf_batch = tokenizer(line[1], max_length=128, padding=True, truncation=True, return_tensors='tf')
            tf_outputs = model(tf_batch)
            tf_predictions = tf.nn.softmax(tf_outputs[0], axis=-1)
            labels = ['5','4','3','2','1']   #好到壞
            label = tf.argmax(tf_predictions, axis=1)
            label = label.numpy()
            for i in range(len(line)):
                pre.append(labels[label[i]])  #儲存
                date1.append(line[0])    #儲存
                break
    #print(date1)
    #print(pre)
    date3 = set(date1)  # date3 刪除相同日期
    list_date3=list(date3) # date3存成LIST
    list_date3.sort(key=date1.index,reverse=True)
    #print(list_date3)
    date2 = np.array(date1)
    score = []
    for i in range(0,len(list_date3)):
        a=0  
        result=np.where(date2==list_date3[i])  #取索引直
        #print(result)
        for j in range(len(result[0])):
            a+=int(pre[j])
        b=round(a/len(result[0]),1)
        score.append(b)
        #print(score)     #計算同個新聞日期，平均分數
    
    # 生成圖與子圖
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=list_date3,y=score))
    fig.update_layout(yaxis_range=[1,5])
    fig.update_layout(title_text=stock[0]+stock[1]+' 的近期新聞預測圖(5是最好)')
    div = opy.plot(fig, auto_open=False, output_type='div')
    
    #預測股價
    #Load Data
    company =targets+'.TW'
    start = dt.datetime(2020,9,1)
    end =dt.datetime(2022,9,1)
    data = yf.download(company,start,end)
    #Prepare Data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(data['Close'].values.reshape(-1,1))
    prediction_days = 60
    x_train = []
    y_train = []
    for x in range(prediction_days, len(scaled_data)):
        x_train.append(scaled_data[x-prediction_days:x, 0])
        y_train.append(scaled_data[x, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    #Build The Model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=50))
    model.add(Dropout(0.2))
    model.add(Dense(units=1)) #Prediction of the next closing value
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=30, batch_size=32)
    '''Test The Model Accuracy on Existing Data'''
    #Load Test Data
    test_start = (dt.datetime.now() - relativedelta(months=12)) #12個月前
    test_end = dt.datetime.now()
    test_data = yf.download(company,test_start,test_end)
    actual_prices = test_data['Close'].values
    total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)
    model_inputs = total_dataset[len(total_dataset)-len(test_data)-prediction_days:].values
    model_inputs = model_inputs.reshape(-1, 1)
    model_inputs = scaler.transform(model_inputs)
    # Make Predictions on Test Data
    x_test = []
    for x in range(prediction_days, len(model_inputs)):
        x_test.append(model_inputs[x-prediction_days:x, 0])
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    predicted_prices = model.predict(x_test)
    predicted_prices = scaler.inverse_transform(predicted_prices)
    
    predicted_prices=predicted_prices.flatten()#降維
    #畫圖
    fig2 = go.Figure()
    fig2.add_traces([go.Scatter(x=test_data.index,y=actual_prices,name='實際股價'),go.Scatter(x=test_data.index,y=predicted_prices,name='預測股價')])
    fig2.update_layout(hovermode='x unified')
    fig2.update_layout(title_text=stock[0]+stock[1]+' 的股價預測走勢圖',)
    div2 = opy.plot(fig2, auto_open=False, output_type='div')
    # Prediction Next Day
    real_data = [model_inputs[len(model_inputs)  -prediction_days:len(model_inputs+1),0]]
    real_data = np.array(real_data)
    real_data = np.reshape(real_data, (real_data.shape[0], real_data.shape[1],1))
    prediction = model.predict(real_data)
    prediction = scaler.inverse_transform(prediction)
    prediction = prediction[0][0]
    msg=metrics.mean_squared_error(predicted_prices, test_data['Close'])
    mag=metrics.mean_absolute_error(predicted_prices, test_data['Close'])
    #MSE 的值越小，說明預測模型描述實驗資料具有更好的精確度。
    #except:
     #   messages.success(request,get_text+' 此股票代非上市股票')
      #  return redirect('predict:predict')
    return render(request,'predict/predict_pic.html',{'fig':div,'fig2':div2,'Prediction':prediction,'msg':msg,'mag':mag})
    