from django.urls import path
from app import views

# app_name = 'app' 


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<str:itemCode>', views.DetailView.as_view(), name='detail'),
    path('list/', views.ListView.as_view(), name='list'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),

    # path('index_f/', views.IndexView_f.as_view(), name='index_f'),
    # path('detail_f/<str:isbn>', views.DetailView_f.as_view(), name='detail_f'),
    # path('create_f/', views.CreateView_f.as_view(), name='create_f'),
]