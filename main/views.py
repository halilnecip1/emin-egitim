# main/views.py

from django.shortcuts import render
from .models import SummerProgram # SummerProgram modelini import ettiğinizden emin olun

def home_view(request):
    """
    Anasayfayı gösterecek olan view. Veritabanından TÜM aktif programları (veya tümünü)
    ve her programın kurslarını çeker ve bunları 'home.html' şablonuna gönderir.
    """
    # Tek bir program almak yerine, tüm programları bir liste olarak alıyoruz.
    # Varsayılan olarak başlangıç tarihine göre azalan sırada (en yeni programlar en üstte)
    # veya id'ye göre sıralayabilirsiniz.
    all_programs = SummerProgram.objects.all().order_by('-start_date') # veya order_by('-id')

    # Eğer sadece aktif programları göstermek isterseniz:
    # all_programs = SummerProgram.objects.filter(is_active=True).order_by('-start_date')


    # Şablona göndereceğimiz verileri bir sözlük (dictionary) içinde topluyoruz.
    context = {
        'programs': all_programs, # Artık tek "program" değil, "programs" adında bir liste
    }

    # request nesnesini, şablonun yolunu ve veri sözlüğümüzü render fonksiyonuna veriyoruz.
    return render(request, 'main/home.html', context)