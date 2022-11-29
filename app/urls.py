from django.urls import path
from app import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('detail/<str:isbn>', views.DetailView.as_view(), name='detail'),
    path('list/', views.ListView.as_view(), name='list'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
]