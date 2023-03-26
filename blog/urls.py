from django.urls import path
from .views import index, detail, article_list

app_name = 'blog'

urlpatterns = [
    path('', index, name='index'),
    path('list/', article_list, name='list'),
    path('detail/<slug:slug>/', detail, name='detail'),
]
