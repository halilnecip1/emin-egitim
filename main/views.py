# main/views.py

from django.shortcuts import render
from .models import SummerProgram, Course # Course modelini de import edin

def home_view(request):
    # Tüm programları alıyoruz, örneğin en son eklenenden başlayarak
    all_programs = SummerProgram.objects.all().order_by('-start_date') # veya order_by('-id')

    # TÜM kursları tek bir liste olarak da alıyoruz
    all_courses = Course.objects.all().order_by('venue_and_time') # Kursları istediğiniz gibi sıralayın

    context = {
        'programs': all_programs, # Tüm SummerProgram'lar
        'all_courses': all_courses, # Tüm kurslar
        # 'cart_item_count' gibi diğer context değişkenleriniz de buraya eklemeyi unutmayın
    }
    return render(request, 'main/home.html', context)