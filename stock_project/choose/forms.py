from django import forms

class efgh(forms.Form):
    stock = forms.CharField(label='',widget=forms.TextInput(attrs={'type':'text','placeholder':'股票代碼/名稱'}))
    start_time = forms.CharField(label='',widget=forms.TextInput(attrs={'type':'date','placeholder':'開始時間'}))
    end_time = forms.CharField(label='',widget=forms.TextInput(attrs={'type':'date','placeholder':'結束時間'}))
