# main/views.py

from django.shortcuts import render
from .models import SummerProgram

def home_view(request):
    """
    Anasayfayı gösterecek olan view. Veritabanından aktif programı
    ve kursları çeker ve bunları 'home.html' şablonuna gönderir.
    """
    program = None
    try:
        # Veritabanından aktif olan ilk programı bulup getiriyoruz.
        # .get() metodu, eğer birden fazla veya hiç bulamazsa hata verir.
        # Bu yüzden try-except bloğu kullanmak daha güvenlidir.
        program = SummerProgram.objects.get(is_active=True)
    except SummerProgram.DoesNotExist:
        # Eğer veritabanında aktif bir program yoksa, program değişkeni None olarak kalır.
        # Bu, sayfanın çökmesini engeller.
        pass

    # Şablona göndereceğimiz verileri bir sözlük (dictionary) içinde topluyoruz.
    context = {
        'program': program,
    }

    # request nesnesini, şablonun yolunu ve veri sözlüğümüzü render fonksiyonuna veriyoruz.
    return render(request, 'main/home.html', context)