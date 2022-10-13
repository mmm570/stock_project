from django import forms

class efgh(forms.Form):
    start_time = forms.CharField(label='',widget=forms.TextInput(attrs={'type':'date','placeholder':'開始時間'}))
    end_time = forms.CharField(label='',widget=forms.TextInput(attrs={'type':'date','placeholder':'結束時間'}))
