# accounts/admin.py

# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student
# Az önce oluşturduğumuz yeni formları import ediyoruz
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    # Admin panelinde yeni kullanıcı oluştururken bizim özel formumuzu kullan
    add_form = CustomUserCreationForm
    # Mevcut bir kullanıcıyı değiştirirken bizim özel formumuzu kullan
    form = CustomUserChangeForm
    # Modelimizi belirtiyoruz
    model = User
    
    # Kullanıcı listeleme ekranında görünecekler
    list_display = ['email', 'telefon', 'first_name', 'last_name', 'is_staff']
    
    # Kullanıcı DEĞİŞTİRME sayfasında görünecek alanlar ve gruplamaları
    # BURASI 'username' HATASINI ÇÖZEN KISIM
    fieldsets = (
        (None, {'fields': ('telefon', 'email', 'password')}),
        ('Kişisel Bilgiler', {'fields': ('first_name', 'last_name')}),
        ('İzinler', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Önemli Tarihler', {'fields': ('last_login', 'date_joined')}),
    )

    # Kullanıcı OLUŞTURMA sayfasında görünecek alanlar
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'telefon', 'email', 'password', 'password2'),
        }),
    )
    
    search_fields = ('email', 'telefon', 'first_name', 'last_name')
    ordering = ('email',)


# Modellerimizi panele kaydediyoruz
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student)