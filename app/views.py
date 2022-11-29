from django.shortcuts import render
from django.views.generic import (View, ListView,CreateView,DeleteView)
from .models import App
from .forms import SearchForm
from .forms import AppForm
import json
import requests
from django.urls import reverse_lazy


# SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksTotal/Search/20170404?format=json&applicationId=1072722666659103303'
SEARCH_URL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1072722666659103303'

syouhinnmei ='シリコンバレー一流プログラマーが教える　Pythonプロフェッショナル大全'
nedan ='2860'
yuarueru ='https://books.rakuten.co.jp/rb/17201602/'


def get_api_data(params):
    api = requests.get(SEARCH_URL, params=params).text
    result = json.loads(api)
    items = result['Items']
    return items

class IndexView(View):
    model = App#モデルを指定する
    template_name = 'app/index.html'#テンプレートを指定する

    def get(self, request, *args, **kwargs):
        
        form = SearchForm(request.POST or None)

        return render(request, 'app/index.html', {
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        form = SearchForm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data['title']
            params = {
                'title': keyword,
                'hits' : 28,
            }
            items = get_api_data(params)
            book_data = []
            for i in items:
                item = i['Item']
                title = item['title']
                image = item['largeImageUrl']
                isbn = item['isbn']
                itemPrice = item['itemPrice']
                query = {
                    'title': title,
                    'image': image,
                    'isbn': isbn,
                    'itemPrice': itemPrice,
                }
                book_data.append(query)

            return render(request, 'app/book.html',{
                'book_data': book_data,
                'keyword': keyword
            })

        return render(request, 'app/index.html',{
            'form': form
        })

class DetailView(View):
    def get(self, request, *args, **kwargs):
        
        isbn = self.kwargs['isbn']
        params = {
            'isbn': isbn
        }

        items = get_api_data(params)
        items = items[0]
        item = items['Item']
        title = item['title']
        image = item['largeImageUrl']
        author = item['author']
        itemPrice = item['itemPrice']
        salesDate = item['salesDate']
        publisherName = item['publisherName']
        size = item['size']
        isbn = item['isbn']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        reviewAverage = item['reviewAverage']
        reviewCount = item['reviewCount']

        syouhinnmei = title

        book_date = {
            'title': title,
            'image': image,
            'author': author,
            'itemPrice': itemPrice,
            'salesDate': salesDate,
            'publisherName': publisherName,
            'size': size,
            'isbn': isbn,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            'reviewAverage': reviewAverage,
            'reviewCount': reviewCount, 
            'average': float(reviewAverage) * 20           
        }
        
        return render(request, 'app/detail.html',{
            'book_data':book_date
        })

        


    

class ListView(ListView):
    template_name = 'app/list.html'
    model = App

class CreateView(CreateView):
    model = App#モデルを指定する
    form_class = AppForm#フォームを指定する
    template_name = "app/create.html"#テンプレートを指定する
    success_url = reverse_lazy("list") #フォーム送信完了後の遷移ページを指定する


    def get_initial(self):
          initial = super().get_initial()
          initial["product_name"] = syouhinnmei
          initial["price"] = nedan
          initial["url"] = yuarueru
          return initial
    

class DeleteView(DeleteView):
    template_name = 'app/delete.html'
    model = App
    success_url = reverse_lazy('list')