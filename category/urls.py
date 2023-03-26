from django.urls import path
from .views import index

app_name = 'category'

urlpatterns = [
    path('', index, name='index')
]
