from django import forms


class trend_forms(forms.Form):
    trend_stock = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'股票代碼/名稱'}))  