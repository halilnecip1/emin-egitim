# main/views.py

from django.shortcuts import render
from .models import SummerProgram # SummerProgram modelini import ettiğinizden emin olun

def home_view(request):
    program = None # Başlangıçta programı boş olarak ayarlıyoruz
    try:
        # Sadece 'is_active=True' olan ilk programı çekiyoruz.
        # Eğer birden fazla aktif programınız varsa, .first() sadece birini seçer.
        program = SummerProgram.objects.filter(is_active=True).first()
        # Eğer program bulunamazsa (yani None gelirse), home.html'deki {% else %} bloğu çalışır.
    except Exception as e:
        # Herhangi bir beklenmedik hata oluşursa loglayabiliriz
        print(f"Program çekilirken hata oluştu: {e}")
        program = None # Hata durumunda programı boş bırak

    context = {
        'program': program, # Tekil 'program' nesnesini gönderiyoruz
    }

    return render(request, 'main/home.html', context)