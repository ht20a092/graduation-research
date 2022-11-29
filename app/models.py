from django.db import models

class App(models.Model):
    product_name = models.CharField('商品名',max_length=255, blank=True)
    price = models.CharField('値段',max_length=255, blank=True)
    url = models.CharField('URL',max_length=255, blank=True)
