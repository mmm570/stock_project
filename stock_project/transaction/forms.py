from django import forms


class login_forms(forms.Form):
    id = forms.EmailField(label='',widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder':'密碼'}))
    
class clickbuy(forms.Form):
    stock_id = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'股票代碼/名稱'}))
    def set(self,val):
        self.fields['stock_id'].widget.attrs.update({'value': val})

class sent(forms.Form):
    stock_id1 = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'股票代碼/名稱'}))    
    choose = forms.ChoiceField(label='買/賣', widget=forms.RadioSelect(attrs={'id':'radio'}),choices=(('buy', '買'),('sell', '賣')),)
    price = forms.CharField(label='價格',widget=forms.TextInput(attrs={'placeholder':'NT$'}))
    count = forms.CharField(label='數量',widget=forms.TextInput(attrs={'placeholder':'張數'}))