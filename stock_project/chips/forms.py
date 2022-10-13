from django import forms

chips_choice1=(("0","代號"),("1","名稱"),("2","價格"),("3","漲跌"),("4","漲跌幅"),("6","周漲跌"),("7","振幅"),("8","最高"),("9","最低"),("10","昨收"),("11","成交量"),("13","成交值(億)"))
chips_choice2=(("0","由小到大排序"),("1","由大到小排序"))
class chips_form(forms.Form):
    table1 = forms.ChoiceField(label='排序方式',choices=chips_choice1)  
    table2 = forms.ChoiceField(label='大小順序',choices=chips_choice2) 
