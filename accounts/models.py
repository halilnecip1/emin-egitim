# accounts/models.py

from django.db import models
# Bu iki import satırını ekliyoruz
from django.contrib.auth.models import AbstractUser, BaseUserManager


# YENİ EKLENEN BÖLÜM: KULLANICI YÖNETİCİSİ
class UserManager(BaseUserManager):
    """
    Django'ya username yerine telefon numarası ile nasıl kullanıcı 
    oluşturacağını öğreten yönetici sınıfı.
    """
    def create_user(self, telefon, email, password=None, **extra_fields):
        """Normal bir kullanıcı oluşturur."""
        if not telefon:
            raise ValueError('Kullanıcıların bir telefon numarası olmalıdır')
        if not email:
            raise ValueError('Kullanıcıların bir e-posta adresi olmalıdır')

        email = self.normalize_email(email)
        user = self.model(telefon=telefon, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telefon, email, password=None, **extra_fields):
        """Süper kullanıcı (admin) oluşturur."""
        # Admin kullanıcı için varsayılan yetkileri ayarlıyoruz
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Süper kullanıcının is_staff=True olmalıdır.')
        # HATA BURADAYDI, DÜZELTİLDİ: extra_gields -> extra_fields
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Süper kullanıcının is_superuser=True olmalıdır.')
        
        # Normal kullanıcı oluşturma fonksiyonunu çağırarak admini yaratıyoruz
        return self.create_user(telefon, email, password, **extra_fields)


# GÜNCELLENEN USER MODELİ
class User(AbstractUser):
    username = None
    email = models.EmailField('e-posta adresi', unique=True)
    telefon = models.CharField('telefon numarası', max_length=15, unique=True)

    USERNAME_FIELD = 'telefon'
    REQUIRED_FIELDS = ['email']

    # YENİ EKLENEN SATIR: Django'ya yeni yönetici sınıfımızı tanıtıyoruz
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.email


# STUDENT MODELİ (Değişiklik yok)
class Student(models.Model):
    GENDER_CHOICES = (
        ('Erkek', 'Erkek'),
        ('Kız', 'Kız'),
    )
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students', verbose_name="Veli")
    first_name = models.CharField("Öğrenci Adı", max_length=100)
    last_name = models.CharField("Öğrenci Soyadı", max_length=100)
    tc_kimlik_no = models.CharField("TC Kimlik No", max_length=11, unique=True)
    school = models.CharField("Okulu", max_length=150)
    grade = models.CharField("Sınıfı", max_length=20)
    gender = models.CharField("Cinsiyet", max_length=5, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"