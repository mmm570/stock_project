from django import forms


class new_forms(forms.Form):
    newUrl = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'yahoo新聞網址'}))  
    
class new_Imgforms(forms.Form):
    newImg = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'股票代碼/名稱'}))  