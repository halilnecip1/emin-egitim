# main/urls.py (Yeni oluşturulan dosya)

from django.urls import path
from .views import home_view

urlpatterns = [
    # Ana dizin ('') için home_view'ı çalıştır. 
    # name='home' ise bu URL'e kod içinde kolayca referans vermemizi sağlar.
    path('', home_view, name='home'),
]