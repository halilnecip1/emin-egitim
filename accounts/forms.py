# accounts/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from .models import Student

# BU FORM, YENİ KULLANICI KAYITLARI İÇİN KULLANILMAYA DEVAM EDECEK
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'telefon', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

# BU FORMU YENİ EKLİYORUZ - ADMİN PANELİ KULLANACAK
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        # Admin panelinde bir kullanıcıyı düzenlerken hangi alanların görüneceği
        fields = ('first_name', 'last_name', 'telefon', 'email')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # Velinin formda doldurmasını istediğimiz alanlar
        # 'parent' alanını buraya dahil ETMİYORUZ, çünkü onu arkada biz atayacağız.
        fields = ['first_name', 'last_name', 'tc_kimlik_no', 'school', 'grade', 'gender']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        # Kullanıcının değiştirmesine izin verdiğimiz alanlar
        fields = ['first_name', 'last_name', 'email', 'telefon']