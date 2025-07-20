# enrollments/urls.py

from django.urls import path
from .views import add_to_cart_view, cart_detail_view, complete_enrollment_view, receipt_upload_view, cart_remove_item_view, cart_clear_view

urlpatterns = [
    # /sepet/ adresine gidince sepet detayını göster
    path('', cart_detail_view, name='cart_detail'),
    # /sepet/ekle/ adresine POST isteği gelince sepete ekle
    path('ekle/', add_to_cart_view, name='add_to_cart'),
    # /sepet/tamamla/ adresine POST isteği gelince kaydı tamamla
    path('tamamla/', complete_enrollment_view, name='complete_enrollment'),
    path('dekont-yukle/<int:enrollment_id>/', receipt_upload_view, name='receipt_upload'),
    path('kaldir/<int:item_index>/', cart_remove_item_view, name='cart_remove_item'),
    path('temizle/', cart_clear_view, name='cart_clear'),
]