from django import forms
from .models import App


class SearchForm(forms.Form):
    title = forms.CharField(label='タイトル', max_length=200, required=True)

class SearchFormm(forms.Form):
    titlee = forms.CharField(label='タイトル', max_length=200, required=True)


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        # fields = ('product_name','price','url','itemCode') 
        fields = ('product_name','price','url','itemCode','price1','price2','price3','price4','price5',)
        # exclude = ('price1','price2','price3','price4','price5',)  #入力項目から商品名、値段、URLを除外

    

    


