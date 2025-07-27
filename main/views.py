# main/views.py

from django.shortcuts import render
from .models import SummerProgram, Course # Course modelini de import edin

def home_view(request):
    """
    Anasayfayı gösterecek olan view. Veritabanından TÜM programları ve TÜM kursları çeker
    ve bunları 'home.html' şablonuna gönderir.
    """
    # Tüm programları başlangıç tarihine göre azalan sırada (en yeniler en başta) alıyoruz.
    all_programs = SummerProgram.objects.all().order_by('-start_date') # veya order_by('-id')

    # TÜM kursları tek bir liste olarak alıyoruz (örneğin yer/saate göre sıralanmış)
    all_courses = Course.objects.all().order_by('venue_and_time')

    context = {
        'programs': all_programs,   # Tüm SummerProgram nesneleri listesi
        'all_courses': all_courses, # Tüm Course nesneleri listesi
        # 'cart_item_count' gibi diğer context değişkenlerinizi de buraya eklemeyi unutmayın
    }

    return render(request, 'main/home.html', context)