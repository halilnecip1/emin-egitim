# enrollments/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Enrollment

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'parent_info', 'course', 'kayit_durumu', 'dekont_goruntule')
    list_filter = ('kayit_durumu', 'course')
    search_fields = ('student__first_name', 'student__last_name', 'parent__email', 'parent__telefon')
    
    # Yönetici panelinde toplu işlem aksiyonlarını tanımlıyoruz
    actions = ['kayitlari_onayla', 'kayitlari_reddet']

    def parent_info(self, obj):
        # Öğrencinin velisinin bilgilerini göstermek için bir fonksiyon
        return f"{obj.parent.first_name} {obj.parent.last_name} ({obj.parent.telefon})"
    parent_info.short_description = 'Veli Bilgisi'

    def dekont_goruntule(self, obj):
        # Yüklenen dekontu admin panelinde küçük bir resim olarak göstermek için
        if obj.dekont:
            return format_html('<a href="{0}" target="_blank"><img src="{0}" width="100px" /></a>', obj.dekont.url)
        return "Dekont Yüklenmedi"
    dekont_goruntule.short_description = 'Yüklenen Dekont'

    def kayitlari_onayla(self, request, queryset):
        # Seçili kayıtların durumunu 'Kayıt Tamamlandı' yapar
        queryset.update(kayit_durumu='KAYIT_TAMAMLANDI')
    kayitlari_onayla.short_description = "Seçili Kayıtları Onayla"

    def kayitlari_reddet(self, request, queryset):
        # Seçili kayıtların durumunu 'Kayıt Reddedildi' yapar
        queryset.update(kayit_durumu='KAYIT_REDDEDILDI')
    kayitlari_reddet.short_description = "Seçili Kayıtları Reddet"