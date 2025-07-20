# enrollments/models.py

from django.db import models
# Diğer uygulamalardaki modelleri buraya import etmemiz gerekiyor
from accounts.models import User, Student
from main.models import Course

# enrollments/models.py

class Enrollment(models.Model):
    STATUS_CHOICES = (
        ('ODEME_BEKLENIYOR', 'Ödeme Bekleniyor'),
        ('ONAY_BEKLENIYOR', 'Kayıt Onayı Bekleniyor'),
        ('KAYIT_TAMAMLANDI', 'Kayıt Tamamlandı'),
        ('KAYIT_REDDEDILDI', 'Kayıt Reddedildi'),
    )

    parent = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Veli")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Öğrenci")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    
    # YENİ EKLENEN SATIR
    total_amount = models.DecimalField("Toplam Tutar", max_digits=10, decimal_places=2, null=True)

    kayit_durumu = models.CharField(
        "Kayıt Durumu",
        max_length=20,
        choices=STATUS_CHOICES,
        default='ODEME_BEKLENIYOR'
    )
    dekont = models.ImageField("Dekont", upload_to='receipts/', null=True, blank=True)
    created_at = models.DateTimeField("Oluşturulma Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme Tarihi", auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.course} ({self.get_kayit_durumu_display()})"