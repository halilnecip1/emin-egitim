# lidersite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # BU SATIR ANASAYFAYI YÖNETİR, MUTLAKA OLMALI
    path('', include('main.urls')),
    
    # BU SATIR KULLANICI İŞLEMLERİNİ (/hesap/...) YÖNETİR, MUTLAKA OLMALI
    path('hesap/', include('accounts.urls')),
    
    # BU SATIR SEPET İŞLEMLERİNİ (/sepet/...) YÖNETİR. 'enrollments.urls' BURADA OLMALI.
    path('sepet/', include('enrollments.urls')),
]

if settings.DEBUG: # <-- Bu kısım ÖNEMLİ
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)