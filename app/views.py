from django.shortcuts import render
from django.views.generic import (View, ListView,CreateView,DeleteView,TemplateView)
from .models import App
from .forms import SearchForm
from .forms import SearchFormm
from .forms import AppForm
import json
import requests
from django.urls import reverse_lazy

from . import models
from . import graph

import matplotlib
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse



# 楽天商品
SEARCH_URL = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?format=json&applicationId=1072722666659103303'

# 楽天ブックス
SEARCH_URLL = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId=1072722666659103303'

syouhinnmei ='シリコンバレー一流プログラマーが教える　Pythonプロフェッショナル大全'
nedan = 2860
yuarueru ='https://books.rakuten.co.jp/rb/17201602/'
cord = ''



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
                'keyword': keyword,
                'hits' : 28,
            }
            items = get_api_data(params)
            book_data = []
            for i in items:
                item = i['Item']
                itemName = item['itemName']
                # imageUrl = item['imageUrl']
                itemCode = item['itemCode']
                itemPrice = item['itemPrice']
                query = {
                    'itemName': itemName,
                    # 'imageUrl': imageUrl,
                    'itemCode': itemCode,
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
        
        itemCode = self.kwargs['itemCode']
        params = {
            'itemCode': itemCode
        }

        items = get_api_data(params)
        items = items[0]
        item = items['Item']
        itemName = item['itemName']
        # imageUrl = item['imageUrl']
        # author = item['author']
        itemPrice = item['itemPrice']
        # salesDate = item['salesDate']
        # publisherName = item['publisherName']
        # size = item['size']
        itemCode = item['itemCode']
        itemCaption = item['itemCaption']
        itemUrl = item['itemUrl']
        # reviewAverage = item['reviewAverage']
        # reviewCount = item['reviewCount']



        book_date = {
            
            'itemName': itemName,
            # 'imageUrl': imageUrl,
            # 'author': author,
            'itemPrice': itemPrice,
            # 'salesDate': salesDate,
            # 'publisherName': publisherName,
            # 'size': size,
            'itemCode': itemCode,
            'itemCaption': itemCaption,
            'itemUrl': itemUrl,
            # 'reviewAverage': reviewAverage,
            # 'reviewCount': reviewCount, 
            # 'average': float(reviewAverage) * 20           
        }
        
        global syouhinnmei
        global nedan
        global yuarueru
        global cord

        syouhinnmei = itemName
        nedan = itemPrice
        yuarueru = itemUrl
        cord = itemCode

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
          initial["itemCode"] = cord
          return initial
    

class DeleteView(DeleteView):
    template_name = 'app/delete.html'
    model = App
    success_url = reverse_lazy('list')





# def setPlt():
#     x = ["7 day ago","6 day ago","5 day ago", "4 day ago", "3 day ago", "2 day ago", "1 day ago"]
#     y = [0, 0,0, 0, 3190, 3190, 3190]
#     plt.bar(x, y, color='#00d5ff')
#     plt.title(r"$\bf{Price Date}$", color='#3407ba')
#     plt.xlabel("")
#     plt.ylabel("price")

# # SVG化
# def plt2svg():
#     buf = io.BytesIO()
#     plt.savefig(buf, format='svg', bbox_inches='tight')
#     s = buf.getvalue()
#     buf.close()
#     return s

# # 実行するビュー関数
# def get_svg(request):
#     setPlt()  
#     svg = plt2svg()  #SVG化
#     plt.cla()  # グラフをリセット
#     response = HttpResponse(svg, content_type='image/svg+xml')
#     return response


class graphView(TemplateView):

    #テンプレートファイル連携
    template_name = 'app/graph.html'

    #変数としてグラフイメージをテンプレートに渡す
    def get_context_data(self, **kwargs):

        #グラフオブジェクト
        qs    = models.App.objects.get(id=1)  #モデルクラス(Appテーブル)読込
        # x     = [x.product_name for x in qs]           #X軸データ
        x     = ["7 day ago","6 day ago","5 day ago", "4 day ago", "3 day ago", "2 day ago", "1 day ago"]         #X軸データ
        # y     = [y.price for y in qs]        #Y軸データ
        y     = [0, 0,0, 0, 3190, 3190, 3190]       #Y軸データ
        chart = graph.Plot_Graph(x,y)          #グラフ作成

        #変数を渡す
        context = super().get_context_data(**kwargs)
        context['chart'] = chart
        return context

    #get処理
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)







#　ここからはyahoo

def get_api_dataa(params):
    api = requests.get(SEARCH_URLL, params=params).text
    result = json.loads(api)
    items = result['Items']
    return items


class IndexView_f(View):
    model = App#モデルを指定する
    template_name = 'app/index_f.html'#テンプレートを指定する

    def get(self, request, *args, **kwargs):
        
        form = SearchFormm(request.POST or None)

        return render(request, 'app/index_f.html', {
            'form': form,
        })
    
    def post(self, request, *args, **kwargs):
        form = SearchFormm(request.POST or None)

        if form.is_valid():
            keyword = form.cleaned_data['titlee']
            params = {
                'title': keyword,
                'hits' : 28,
            }
            items = get_api_dataa(params)
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

            return render(request, 'app/book_f.html',{
                'book_data': book_data,
                'keyword': keyword
            })

        return render(request, 'app/index_f.html',{
            'form': form
        })


class DetailView_f(View):
    def get(self, request, *args, **kwargs):
        
        isbn = self.kwargs['isbn']
        params = {
            'isbn': isbn
        }

        items = get_api_dataa(params)
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
            'average': float(reviewAverage) * 20   ,
        }

        global syouhinnmei
        global nedan
        global yuarueru
        global yuarueru

        syouhinnmei = title
        nedan = itemPrice
        yuarueru = itemUrl

        return render(request, 'app/detail_f.html',{
            'book_data':book_date
        })


        
    

class ListView_f(ListView):
    template_name = 'app/list_f.html'
    model = App


class CreateView_f(CreateView):
    model = App#モデルを指定する
    form_class = AppForm#フォームを指定する
    template_name = "app/create_f.html"#テンプレートを指定する
    success_url = reverse_lazy("list") #フォーム送信完了後の遷移ページを指定する


    def get_initial(self):
          initial = super().get_initial()
          initial["product_name"] = syouhinnmei
          initial["price"] = nedan
          initial["url"] = yuarueru
          return initial

