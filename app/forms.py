from django import forms
from .models import App


class SearchForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=200, required=True)

class SearchFormm(forms.Form):
    titlee = forms.CharField(label='タイトル', max_length=200, required=True)


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ('product_name','price','url',) 
        #exclude = ('product_name','price','url',)  #入力項目から商品名、値段、URLを除外

    

    


