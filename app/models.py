from django.db import models

class App(models.Model):
    product_name = models.CharField('商品名',max_length=255, blank=True)
    price = models.CharField('値段',max_length=255, blank=True)
    url = models.CharField('URL',max_length=255, blank=True)
    itemCode = models.CharField('アイテムコード',max_length=255, blank=True)

    price1 = models.CharField('値段データ１',max_length=255, blank=True)
    price2 = models.CharField('値段データ２',max_length=255, blank=True)
    price3 = models.CharField('値段データ３',max_length=255, blank=True)
    price4 = models.CharField('値段データ４',max_length=255, blank=True)
    price5 = models.CharField('値段データ５',max_length=255, blank=True)

