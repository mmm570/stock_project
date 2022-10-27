from django.shortcuts import render,redirect
from transaction.forms import sent,login_forms,clickbuy
from django.contrib import messages
import twstock
import other
from django.db import connection

#django session
#https://iter01.com/672416.html 
#https://ithelp.ithome.com.tw/m/articles/10212461

def transaction(request):
    if 'saveid' in request.session:
        return redirect('transaction:btn1Create')
    return render(request,'transaction/transaction.html',{'who_login':login_forms()})
    
def login_register(request):
    if request.POST:
        if 'login' in request.POST:
            idVal = request.POST["id"]
            passwordVal = request.POST["password"]
            
            with connection.cursor() as cursor:
                # 查詢資料SQL語法
                command = "SELECT * FROM charts where id=%s "
                cursor.execute(command,[idVal])
                result = cursor.fetchone()
                if result is None:
                    messages.success(request,'尚未註冊')
                    return redirect('transaction:transaction')
                else:
                    var1 = idVal
                    var11=result[0]
                    var2 = passwordVal
                    var22=result[1]
                    if (var1) ==(var11) and (var2) == (var22):
                        request.session['saveid']=var1
                        messages.success(request,idVal+'，登入成功')
                        #return render(request,'transaction/transaction2.html',{'id':idVal})
                        return redirect('transaction:btn1Create')
                    else:
                        messages.success(request,'帳號或密碼錯誤')
                        return redirect('transaction:transaction')
        else:
            idVal = request.POST["id"]
            passwordVal = request.POST["password"]
            
            try:
                with connection.cursor() as cursor:
                    command = "INSERT INTO charts(id,password,allmoney)VALUES(%s, %s, 10000000)"
                    cursor.execute(command,[idVal,passwordVal])
                    connection.commit()#回傳結果到另一個頁面  
                messages.success(request,idVal+'註冊成功')
                return redirect('transaction:transaction')
            except:
                with connection.cursor() as cursor:
                    # 查詢資料SQL語法
                    command = "SELECT * FROM charts where id=%s "
                    cursor.execute(command,[idVal])
                    result = cursor.fetchone()
                messages.success(request,idVal+'，帳號已註冊，請直接登入')
                return redirect('transaction:transaction')
    else:
        messages.success(request,'尚未登入')
        return redirect('transaction:transaction')     
        
def btn1Create(request):
     return render(request, 'transaction/btn1Create.html',{'who':sent(),'stock_num':clickbuy(),'id':request.session['saveid']})
def clickbuy1(request):#查詢
    try:
        get_text = request.GET["stock_id"]
        have=other.sql(get_text)
        stockid=have[0]
        stock_name=have[1]
        title_text=stockid+' '+stock_name
        stock=twstock.realtime.get(stockid)
        best_bid_price=stock['realtime']['best_bid_price']
        best_bid_price=[round(float(i),3) for i in best_bid_price]
        best_ask_price=stock['realtime']['best_ask_price']
        best_ask_price=[round(float(i),3) for i in best_ask_price]
        all_price=zip(best_bid_price,best_ask_price)
        newform = clickbuy()
        newform.set(get_text)
        request.session['ask']=best_ask_price[0]
        request.session['have0']=stockid
    except:
        messages.success(request,get_text+' 此股票代非上市股票')
        return redirect('transaction:btn1Create')
    return render(request, 'transaction/btn1Create.html',{'who':sent(),'stock_num':newform,'result':title_text,'result_price':all_price,'id':request.session['saveid'],'have':have,'best_ask_price':best_ask_price[0]})
def buy_sell(request):#查詢   
    try:    
    
        get_text = request.session['have0']
        have=other.sql(get_text)
        stockid=have[0]
        stock_name=have[1]
        title_text=stockid+' '+stock_name
            
        choose_buy_sell = request.GET["choose"]
        stock_price = str(request.session['ask'])
        buy_sell_count = request.GET["count"]
        saveid=request.session['saveid']
        stock=twstock.realtime.get(stockid)               
        if choose_buy_sell   == 'buy' : #買進
            with connection.cursor() as cursor:
                #-------------------------------------------------
                command = "SELECT allmoney FROM charts WHERE id = %s"#判斷金額足夠
                cursor.execute(command,[saveid])
                result = cursor.fetchone()[0]
                if float(result) < float(stock_price)*int(buy_sell_count)*1000:
                    buy_sell_result="金額不足無法買進"
                else:
                    #-------------------------------------------------
                    command = "SELECT * FROM stock " #抓取資料庫資料行數
                    cursor.execute(command)
                    result = cursor.fetchall()
                    if len(result) == 0 :
                        id1=1
                    else:
                        id1=result[-1][0]+1
                    #-------------------------------------------------
                                                    #抓取3種輸入資料 代碼 價格 張數
                    command = "insert into stock(id1,stockmoney1,stockmoney2,stockmoney3,stock_id) values(%s,%s,%s,%s,%s)"
                    cursor.execute(command,[id1,stockid,stock_price,buy_sell_count,saveid])
                    
                    command = "SELECT * FROM record " #抓取資料庫資料行數
                    cursor.execute(command)
                    result = cursor.fetchall()
                    if len(result) == 0 :
                        id1=1
                    else:
                        id1=result[-1][0]+1 #-1:最後一筆資料\0:id1[]
                        
                    command = "insert into record(id1,stockmoney1,stockmoney2,stockmoney3,stock_id,date1,buy_sell) values(%s,%s,%s,%s,%s,now(),'買進')"
                    cursor.execute(command,[id1,stockid,stock_price,buy_sell_count,saveid])
                    
                    command = "SELECT * FROM record_1 " #抓取資料庫資料行數
                    cursor.execute(command)
                    result = cursor.fetchall()
                    if len(result) == 0 :
                        id1=1
                    else:
                        id1=len(result)+1
                    print(id1)
                    command = "insert into record_1(id1,stockmoney1,stockmoney2,stockmoney3,stock_id,date1,buy_sell) values(%s,%s,%s,%s,%s,now(),'買進')"
                    cursor.execute(command,[id1,stockid,stock_price,buy_sell_count,saveid])
                    #------------------------------------------------- 修改原始金額
                    command = "SELECT allmoney FROM charts WHERE id = %s"    
                    cursor.execute(command,[saveid])
    
                    result1 = cursor.fetchone()
                    arr1 = float(stock_price)*int(buy_sell_count)*1000
                    result2 = float(result1[0]) - arr1
                    command = "UPDATE charts SET allmoney = %s WHERE id = %s"
                    cursor.execute(command,[result2, saveid])
    
                    #-------------------------------------------------
                    connection.commit() 
                    
                    buy_sell_result=("已買出 :  "+title_text+"    /價格為 : "+stock_price+'  /張數 : '+buy_sell_count+'張') #顯示買了甚麼
        #買進的底
        if choose_buy_sell == 'sell' :                                  #賣出
            
            with connection.cursor() as cursor:
                command = "SELECT stockmoney1 FROM stock where (stock_id=%s)and(stockmoney1=%s)"
                cursor.execute(command,[saveid,stockid])
                result = cursor.fetchone()      #result[0] 股票代碼
            if result is None:
                buy_sell_result=('您並未擁有'+title_text+'股票')
            else:
                if result[0] == stockid:
                    #connection.commit()    #connection.close()                     
                    with connection.cursor() as cursor: 
                        command = "SELECT sum(stockmoney3) FROM stock GROUP BY (stock_id=%s)and(stockmoney1=%s)" 
                        cursor.execute(command,[saveid,stockid])
                        result5 = cursor.fetchall()  #加總股票張數(庫存)
                        connection.commit()    
                    if int(buy_sell_count)<=int(result5[-1][0]):#如果賣出的張數<=庫存張數
                                            
                        with connection.cursor() as cursor: 
                        
                            command = "SELECT stockmoney1,stockmoney2,stockmoney3 FROM stock where (stock_id=%s)and(stockmoney1=%s)"
                            cursor.execute(command,[saveid,stockid])
                            result = cursor.fetchall() #代碼 張數 價格
                            connection.commit()    
                            
                        a1=0
                        for i in range (0,len(result)):
                            a1+=float(result[i][1])*float(result[i][2])
                        a1=round(a1/len(result),2)  #平均成本(張)
        
        
                        #抓原本資產 加上賺的 刪原本的股票 新增剩餘的股票
                        #connection.commit()    #connection.close()                     
                        with connection.cursor() as cursor: 
                            command = "SELECT allmoney FROM charts WHERE id = %s"#原本資產
                            cursor.execute(command,[saveid])
                            result3 = cursor.fetchone()
                        connection.commit()    
                        
                        result4=int(result3[0])
                        #connection.commit()    #connection.close()                     
                        with connection.cursor() as cursor: 
                            command = "UPDATE charts SET allmoney = %s WHERE id = %s"#加上賺的
                            result4 += float(stock_price)*int(buy_sell_count)*1000
                            cursor.execute(command,[result4, saveid])
                        connection.commit()
                          
                        if int(result5[-1][0])-int(buy_sell_count)==0:
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor: 
                                command = "DELETE FROM stock WHERE (stock_id=%s)and(stockmoney1=%s)"
                                cursor.execute(command,[saveid,stockid])
                            connection.commit()    
                            
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                command = "SELECT * FROM record " #抓取資料庫資料行數
                                cursor.execute(command)
                                result = cursor.fetchall()
                            connection.commit()    
                             
                            if len(result) == 0 :
                                id1=1
                            else:
                                id1=result[-1][0]+1
                                
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                command = "insert into record(id1,stockmoney1,stockmoney2,stockmoney3,stock_id,date1,buy_sell) values(%s,%s,%s,%s,%s,now(),'賣出')"
                                cursor.execute(command,[id1,stockid,stock_price,buy_sell_count, saveid])
                            connection.commit()    
                            
        
                            #------
        
                            id2=0
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                command = "SELECT buy_sell_1 FROM record_1 ORDER BY buy_sell_1 DESC nulls last" #抓取資料庫資料行數
                                cursor.execute(command)
                                result1 = cursor.fetchall()
                            connection.commit()    
                                 
                            
                            if result1[0][0] == None :
                                id2=1
                            else:
                                id2=result1[0][0]+1
                                
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:    
                                
                                command = "SELECT * FROM record_1 " #抓取資料庫資料行數
                                cursor.execute(command)
                                result = cursor.fetchall()
                            connection.commit()    
                              
                            if len(result) == 0 :
                                id1=1
                            else:
                                id1=result[-1][0]+1
                            #------
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:  
                                command = "insert into record_1(id1,stockmoney1,stockmoney2,stockmoney3,stock_id,date1,buy_sell,buy_sell_1) values(%s,%s,%s,%s,%s,now(),'賣出',%s)"
                                cursor.execute(command,[id1,stockid,stock_price,buy_sell_count,saveid,id2])
                            connection.commit()
                              
        
                        if int(result5[-1][0])-int(buy_sell_count)>0:
                            mon= int(result5[-1][0])-int(buy_sell_count)
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor: 
                                command = "DELETE FROM stock WHERE (stock_id=%s)and(stockmoney1=%s)"
                                cursor.execute(command,[saveid,stockid])
                            connection.commit()    
                                
                            
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                command = "SELECT * FROM record " #抓取資料庫資料行數
                                cursor.execute(command)
                                result = cursor.fetchall()
                            connection.commit()    
                               
                            
                            if len(result) == 0 :
                                id1=1
                            else:
                                id1=result[-1][0]+1
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                
                                command = "insert into record(id1,stockmoney1,stockmoney2,stockmoney3,stock_id,date1,buy_sell) values(%s,%s,%s,%s,%s,now(),'賣出')"
                                cursor.execute(command,[id1,stockid,stock_price,buy_sell_count,saveid])
                            connection.commit()    
                             
                            
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                
                                command = "SELECT * FROM record_1 " #抓取資料庫資料行數
                                cursor.execute(command)
                                result = cursor.fetchall()
                            connection.commit()
                            
                            if len(result) == 0 :
                                id1=1
                            else:
                                id1=result[-1][0]+1
        
                            id2=0
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:
                                
                                command = "SELECT buy_sell_1 FROM record_1 ORDER BY buy_sell_1 DESC nulls last" #抓取資料庫資料行數
                                cursor.execute(command)
                                result1 = cursor.fetchall()
                            connection.commit()    
    
                            if result1[0][0] == None :
                                id2=1
                            else:
                                id2=result1[0][0]+1
                                
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor:     
                                command = "SELECT * FROM record_1 " #抓取資料庫資料行數
                                cursor.execute(command)
                                result = cursor.fetchall()
                            connection.commit() 
                            
                            if len(result) == 0 :
                                id1=1
                            else:
                                id1=result[-1][0]+1                        #------
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor: 
                                command = "insert into record_1(id1,stockmoney1,stockmoney2,stockmoney3,stock_id,date1,buy_sell,buy_sell_1) values(%s,%s,%s,%s,%s,now(),'賣出',%s)"
                                cursor.execute(command,[id1,stockid,stock_price,buy_sell_count,saveid,id2])
        
                            connection.commit()
                            
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor: 
                                command = "SELECT * FROM stock " #抓取資料庫資料行數
                                cursor.execute(command)
                                result = cursor.fetchall()
                            connection.commit()
                            
                            if len(result) == 0 :
                                id1=1
                            else:
                                id1=result[-1][0]+1
        
                            #connection.commit()    #connection.close()                     
                            with connection.cursor() as cursor: 
                                
                                command = "insert into stock(id1,stockmoney1,stockmoney2,stockmoney3,stock_id) values(%s,%s,%s,%s,%s)"
                                cursor.execute(command,[id1,stockid,a1,mon, saveid])
        
        
                            connection.commit()
                        else:
                            buy_sell_result=("輸入錯誤")
                    else:
                        buy_sell_result=("輸入錯誤")
        #--------------------------------------------------
                    a=''
                    s='已實現'
                    #connection.commit()    #connection.close()                     
                    with connection.cursor() as cursor:        
                        command = "SELECT * FROM record_1 where stock_id=%s and stockmoney1=%s and buy_sell='賣出'"
                        cursor.execute(command,[saveid,stockid])
                        result1 = cursor.fetchall()
                        connection.commit()                  
                        
                    a=result1[-1][3]#找資料庫record_1賣出的有多少張數
                    print('123')
                    print(a)
                    print(result1)
                    print("-------------------------") 
                    
                    
                    with connection.cursor() as cursor:    
                        command = "SELECT * FROM record_1 where stock_id=%s and stockmoney1=%s and buy_sell='買進'"
                        cursor.execute(command,[saveid,stockid])
                        result2 = cursor.fetchall()
                        connection.commit()                  
                        print(result2)#找資料庫record_1買進的有多少列
                        print('\n')
                        print("-------------------------") 
                    
                    with connection.cursor() as cursor:   
                        command = "SELECT * FROM record_1 where stock_id=%s and stockmoney1=%s"
                        cursor.execute(command,[saveid,stockid])
                        
                        result5 = cursor.fetchall()
                        connection.commit()                  
                        
                        
                    for i in range(0,len(result2)):
                        id2=0
                        
                        with connection.cursor() as cursor:
                            command = "SELECT buy_sell_1 FROM record_1 ORDER BY buy_sell_1 DESC nulls last" #抓取資料庫資料行數
                            cursor.execute(command)
                            
                            result1 = cursor.fetchall()
                        print(result1)
                        id2=result1[0][0]
                        connection.commit()                  
                        
                        print("result2[i][3]",str(result2[i][3]),"A",str(a))
                        if int(result2[i][3]) > a:
                            
                            with connection.cursor() as cursor:
                                command = "update record_1 set stockmoney3=(%s - %s) where id1 =%s"
                                cursor.execute(command,[result2[i][3],a,result2[i][0]])
            
                            connection.commit()                  
                            
                            with connection.cursor() as cursor:
                                command = "insert into record_1 values(%s,%s,%s,%s,%s,%s,%s,%s)"
                                cursor.execute(command,[(result5[-1][0]+1),result2[i][1],result2[i][2],a,result2[i][4],result2[i][5],s,id2])
                            connection.commit()
                            break
                        if int(result2[i][3]) == a:
                            
                            with connection.cursor() as cursor:
                                command = "update record_1 set buy_sell=%s  where id1 =%s"
                                cursor.execute(command,[s,result2[i][0]])
                            connection.commit()
                            
                            with connection.cursor() as cursor:
                                command = "update record_1 set buy_sell_1=%s  where id1 =%s"
                                cursor.execute(command,[id2,result2[i][0]])
                            connection.commit()
            
                            break
                        if int(result2[i][3]) <a:
                            
                            with connection.cursor() as cursor:
                                command = "update record_1 set buy_sell=%s where id1 =%s"
                                cursor.execute(command,[s,result2[i][0]])
                            connection.commit()
                            
                            with connection.cursor() as cursor:
                                print('aaa')
                                print(result2[i][0])
                                command = "update record_1 set buy_sell_1=%s  where id1 =%s"
                                cursor.execute(command,[id2,result2[i][0]])
                            connection.commit()
                            a=int(a)-int(result2[i][3])
                            a=str(a)       
                                #-------------------------------------------------- 
                    buy_sell_result=("已賣出 :  "+title_text+"    /價格為 : "+stock_price+'  /張數 : '+buy_sell_count+'張') #顯示買了甚麼
        del request.session["have0"]
        del request.session["ask"]
    except:
         messages.success(request,'請先完成 STEP 1')
         return redirect('transaction:btn1Create')    
    return render(request, 'transaction/btn1Create.html',{'who':sent(),'stock_num':clickbuy(),'buy_sell_result':buy_sell_result,'id':request.session['saveid']})
def btn2Create(request):
    saveid=request.session['saveid']
    
    with connection.cursor() as cursor:
        command = "SELECT stockmoney1  FROM stock where stock_id=%s group by stockmoney1"
        cursor.execute(command,[saveid])
        result = cursor.fetchall()      #result[0] 股票代碼
    #result123=""
    result123=[]
    for i in range(0,len(result)):
        r=[]
        stock=twstock.realtime.get(result[i][0]) 
        a1=round(float(stock['realtime']['best_ask_price'][0]),2)
        with connection.cursor() as cursor:
            command = "SELECT sum(cast (stockmoney3 as int)) FROM stock where stock_id=%s GROUP BY stockmoney1" 
            cursor.execute(command,[saveid])
            result5 = cursor.fetchall()  #加總股票張數(庫存)
            a2=round(float(result5[i][0]),2)            #張數
            a3=round(a1*a2*1000,2)                      #市價
            command = "SELECT sum(cast (stockmoney2 as float)*cast (stockmoney3 as float)*1000) FROM stock where stockmoney1=%s" 
            cursor.execute(command,[result[i][0]])
            result6 = cursor.fetchone()       
                   #成本
            a4=(a3  -  float(  result6[0]  ) ) / float( result6[0])   
            a5= round((a4*100),2)
        r.append(stock['info']['name']+" "+result[i][0] )
        r.append(str(a3))
        r.append(str(a5)+'%')
        result123.append(r)
    
    
    with connection.cursor() as cursor:
        command = "SELECT allmoney FROM charts where id=%s " 
        cursor.execute(command,[saveid])
        result7 = cursor.fetchone()
        if result7 is None:
            cash=0
        else:
            cash=round(float(result7[0]))
        result_money = ('現金資產'+"  "+str(cash))
        
        command = "SELECT sum(cast(stockmoney2 as float)*cast(stockmoney3 as float)*1000) FROM stock where  stock_id=%s" 
        cursor.execute(command,[saveid])
        result8 = cursor.fetchone()
        if result8[0] is None:
            stock_money=0
        else:
            stock_money=int(result8[0])
        result_stock= ('證券資產'+"  "+str(stock_money))
        asset=stock_money+cash
        result_result=('淨資產'+"  "+str(asset) )
        a3=0
        for i in range(0,len(result)):
            stock=twstock.realtime.get(result[i][0])
            a1=round(float(stock['realtime']['best_ask_price'][0]),2)#市價
            with connection.cursor() as cursor:
                command = "SELECT sum(cast(stockmoney3 as int)) FROM stock where stock_id=%s GROUP BY stockmoney1" 
                cursor.execute(command,[saveid])
                result9 = cursor.fetchall()  #加總股票張數(庫存)
                a2=round(float(result9[i][0]),2)            #張數
                a3+=round(a1*a2*1000,2)                      #市值(總計全部)
    get_money=int(a3) - stock_money
    result456=('獲利'+"  "+ str(get_money))
    
    
    if stock_money !=0:
        rate=round((get_money / stock_money)*100,2)
    else:
        rate=0
    result_end=('總報酬率'+"  "+str(rate)+"%")
    return render(request, 'transaction/btn2Create.html',{'result123':result123,'result_money':result_money,'result_stock':result_stock,'result_result':result_result,'result456':result456,'result_end':result_end,'id':request.session['saveid']})
def btn3Create(request):
    saveid=request.session['saveid']
    
    with connection.cursor() as cursor:
        command = "SELECT * FROM record where stock_id=%s order by date1 desc" 
        cursor.execute(command,[saveid])
        result10 = cursor.fetchall()
    text1=[]
    text2=[]
    for i in range(0,len(result10)):
        for j in range(7):
            if j == 0 or j == 4 :
                continue
            if j == 3:
                text1.append(str(result10[i][j])+"張")
                continue
            text1.append(str(result10[i][j]))
        text2.append(text1) 
        text1=[]  
    result=text2
    return render(request, 'transaction/btn3Create.html',{'id':request.session['saveid'],'result':result})
def btn4Create(request):
    saveid=request.session['saveid']
    
    with connection.cursor() as cursor:
        command = "SELECT stockmoney1 ,(sum(stockmoney2*stockmoney3))/sum(stockmoney3),sum(stockmoney3) FROM stock where stock_id=%s GROUP BY stockmoney1 " 
        cursor.execute(command,[saveid])
        result10 = cursor.fetchall()
        
    text3=[]
    for i in range(0,len(result10)):
        t=[]
        stock=twstock.realtime.get(result10[i][0])   
        a1=round(float(stock['realtime']['best_ask_price'][0]),2)#現價
        t.append(stock['info']['name']+" ")
        a2=(a1*1000-float(result10[i][1])*1000)*float(result10[i][2])#總損益
        a3=(a1*1000-float(result10[i][1])*1000)
        a4= round(a3/(float(result10[i][1])*1000)*100,2)#報酬率
        t[0]+=str(result10[i][0])
        t.append(str(a2))
        t.append(str(a4)+"%")
        t.append(str(result10[i][1]))
        t.append(str(result10[i][2]))    
        t.append(a1)
        text3.append(t)
        
    return render(request, 'transaction/btn4Create.html',{'text3':text3,'id':saveid})
def btn5Create(request):
    saveid=request.session['saveid']
    
    with connection.cursor() as cursor:
        command = "SELECT stockmoney1 ,(sum(stockmoney2*stockmoney3))/sum(stockmoney3),sum(stockmoney3) FROM stock where stock_id=%s GROUP BY stockmoney1 " 
        cursor.execute(command,[saveid])
        result11 = cursor.fetchall()
    text4=[]
    text5=[]
    text6=[]
    text7=[]
    a7=0
    a8=0
    for i in range(0,len(result11)):
        stock=twstock.realtime.get(result11[i][0])   
        a1=round(float(stock['realtime']['best_ask_price'][0]),2)#現價
        text4.append(stock['info']['name']+' '+str(result11[i][0]))
        for j in range(3):
            a2=(a1*1000-float(result11[i][1])*1000)*float(result11[i][2])#總損益
            a3=(a1*1000-float(result11[i][1])*1000)
            a4= round(a3/(float(result11[i][1])*1000)*100,2)#報酬率
            a5=float(result11[i][1])*float(result11[i][2])*1000#買入成本
            a6=a1*float(result11[i][2])*1000#預估賣出收益
            if j == 0 :
                text4.append(round((a2),2))
                text4.append(str(round((a4),2))+"%")
            else:
                text4.append(round((result11[i][j]),2))
        a7+=a5#總買入成本
        a8+=a6#總賣出收益    
        text4.append(round((a1),2))
        text4.append(round((a5),2))
        text4.append(round((a6),2))
        text5.append(text4)
        text4=[]
    result1=str(a7)
    result2=str(a8)
    
    b=0 
    c=0
    #text5=''
    rate=0
    with connection.cursor() as cursor:
        command = "SELECT stockmoney1,buy_sell_1  FROM record_1 where stock_id=%s and buy_sell = '賣出' order by buy_sell_1 desc nulls last" 
        cursor.execute(command,[saveid])
        result13 = cursor.fetchall()
        print(result13)
        if not result13:
            text7=[["無已實現損益"]]
        else:
            for i in range(1,int(result13[0][1])+1):
                n=i
                command = "SELECT stockmoney1,stockmoney2,stockmoney3,buy_sell_1  FROM record_1 where stock_id=%s and buy_sell = '賣出' and buy_sell_1=%s " 
                cursor.execute(command,[saveid,n])
                result11 = cursor.fetchall()
                if not result11:
                    continue
                else:
                    d=result11[0][1]
                    for i in range (0,len(result11)):
                        b=int(result11[i][1])*int(result11[i][2])*1000 #賣出收益
                    command = "SELECT stockmoney1,stockmoney2,stockmoney3  FROM record_1 where stock_id=%s and buy_sell = '已實現' and buy_sell_1=%s" 
                    cursor.execute(command,[saveid,n])
                    result12 = cursor.fetchall()
                    if not result12:
                        continue
                    else:
                        c=0
                        for i in range (0,len(result12)):
                            c+=int(result12[i][1])*int(result12[i][2])*1000 #買入成本
                        pro=b-c #損益
                        rate=str(round((b-c)/c*100,2))
                        stock=twstock.realtime.get(result12[i][0])
                        text6.append(stock['info']['name']+str(result12[i][0]))
                        text6.append(str(pro))
                        text6.append(rate+'%')
                        text6.append(str(result12[i][2]))
                        text6.append(str(result12[i][1]))
                        text6.append(str(d))
                        text6.append(str(c))
                        text6.append(str(b))
                        text7.append(text6)
                        text6=[]
    return render(request, 'transaction/btn5Create.html',{'result1':result1,'result2':result2,'text5':text5,'text7':text7,'id':saveid})

def logout(request):
    messages.success(request,request.session['saveid']+'，已登出')
    request.session.flush() 
    return redirect('transaction:transaction')