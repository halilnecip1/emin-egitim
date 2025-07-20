# accounts/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view, student_list_view, student_add_view, get_students_json_view, payment_history_view, profile_update_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('panelim/ogrencilerim/', student_list_view, name='student_list'),
    path('panelim/ogrenci-ekle/', student_add_view, name='student_add'),
    path('panelim/odemelerim/', payment_history_view, name='payment_history'),
    # Kayıt olma sayfası
    path('kayit/', register_view, name='register'),
    
    # Giriş yapma sayfası (Django'nun hazır view'ını kullanıyoruz)
    path('giris/', LoginView.as_view(template_name='accounts/login.html'), name='login'),

    # Çıkış yapma işlemi (Django'nun hazır view'ını kullanıyoruz)
    path('cikis/', LogoutView.as_view(next_page='home'), name='logout'),

    path('api/get-students/', get_students_json_view, name='get_students_json'),
    path('panelim/bilgilerim/', profile_update_view, name='profile_update'),    
    path(
        'panelim/sifre-degistir/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/password_change_form.html',
            success_url='/hesap/panelim/sifre-degistir/basarili/' # Başarılı olunca gidilecek adres
        ),
        name='password_change'
    ),
    path(
        'panelim/sifre-degistir/basarili/',
        auth_views.PasswordChangeDoneView.as_view(
            template_name='accounts/password_change_done.html'
        ),
        name='password_change_done'
    ),
]