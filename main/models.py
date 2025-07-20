# main/models.py

from django.db import models

class SummerProgram(models.Model):
    title = models.CharField("Başlık", max_length=200, default="YAZINA DEĞER KAT 2025 YAZ OKULLARI")
    location = models.CharField("Konum", max_length=100, default="İSTANBUL")
    price = models.DecimalField("Ücret", max_digits=10, decimal_places=2, default=16000.00)
    start_date = models.DateField("Başlangıç Tarihi", null=True, blank=True)
    
    # YENİ EKLENEN SATIR
    end_date = models.DateField("Bitiş Tarihi", null=True, blank=True)
    
    poster = models.ImageField("Afiş Görseli", upload_to='posters/', null=True, blank=True)
    
    is_active = models.BooleanField("Aktif Program mı?", default=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    # Hangi ana programa bağlı olduğunu belirtiyoruz
    program = models.ForeignKey(SummerProgram, on_delete=models.CASCADE, related_name='courses')
    venue_and_time = models.CharField("Yer / Saat", max_length=255)
    grade_range = models.CharField("Sınıf Aralığı", max_length=100)
    capacity = models.PositiveIntegerField("Kontenjan", default=100)

    def __str__(self):
        return f"{self.program.title} - {self.venue_and_time}"
    
class ProgramSection(models.Model):
    # Bu bölümün hangi ana programa ait olduğunu belirtiyoruz
    program = models.ForeignKey(SummerProgram, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField("Başlık", max_length=100) # Örn: AMAÇ, KAZANIMLAR
    content = models.TextField("İçerik")
    order = models.PositiveIntegerField("Sıralama", default=0, help_text="Bölümlerin gösterileceği sıra (küçükten büyüğe)")

    class Meta:
        # Bölümleri 'order' alanına göre sırala
        ordering = ['order']

    def __str__(self):
        return f"{self.program.title} - {self.title}"
    
