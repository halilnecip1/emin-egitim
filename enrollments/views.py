# enrollments/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from main.models import Course
from accounts.models import Student
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Enrollment
from django.shortcuts import get_object_or_404
from .forms import ReceiptUploadForm

@login_required
def add_to_cart_view(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        student_id = request.POST.get('student_id')

        if not course_id or not student_id:
            return JsonResponse({'success': False, 'message': 'Kurs veya öğrenci seçilmedi.'})

        # Session'dan sepeti al, yoksa boş bir liste oluştur
        cart = request.session.get('cart', [])
        
        # Bu öğrencinin bu kursa zaten eklenip eklenmediğini kontrol et
        for item in cart:
            if item['course_id'] == course_id and item['student_id'] == student_id:
                return JsonResponse({'success': False, 'message': 'Bu öğrenci bu kursa zaten eklenmiş.'})

        # Sepete yeni ürünü ekle
        cart.append({'course_id': course_id, 'student_id': student_id})
        # Session'ı güncelle
        request.session['cart'] = cart

        return JsonResponse({
            'success': True, 
            'message': 'Kurs sepete eklendi!',
            'cart_item_count': len(cart)
        })
    
    return JsonResponse({'success': False, 'message': 'Geçersiz istek.'})

@login_required
def cart_detail_view(request):
    cart = request.session.get('cart', [])
    detailed_cart_items = []
    total_price = 0

    

    for item in cart:
        try:
            course = Course.objects.get(id=item['course_id'])
            student = Student.objects.get(id=item['student_id'], parent=request.user) # Güvenlik için veli kontrolü
            
            detailed_cart_items.append({
                'course': course,
                'student': student
            })
            total_price += course.program.price
        except (Course.DoesNotExist, Student.DoesNotExist):
            # Eğer bir kurs veya öğrenci veritabanında bulunamazsa (silinmişse vb.)
            # Hatalı veriyi sepetten temizlemek iyi bir pratiktir.
            # Şimdilik bu kısmı basit tutuyoruz.
            pass
            
    context = {
        'detailed_cart_items': detailed_cart_items,
        'total_price': total_price
    }
    return render(request, 'enrollments/cart_detail.html', context)

@login_required
def complete_enrollment_view(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        if not cart:
            return redirect('home')

        for item in cart:
            try:
                course = Course.objects.get(id=item['course_id'])
                student = Student.objects.get(id=item['student_id'], parent=request.user)

                # Veritabanında yeni bir Kayıt (Enrollment) nesnesi oluştur
                Enrollment.objects.create(
                    parent=request.user,
                    student=student,
                    course=course,
                    total_amount=course.program.price,
                    # Diğer alanlar (kayit_durumu) modelde belirttiğimiz varsayılan değeri alacak
                )
            except (Course.DoesNotExist, Student.DoesNotExist):
                # Hatalı veri varsa atla
                pass
        
        # İşlem bittikten sonra sepeti temizle
        del request.session['cart']
        
        messages.success(request, "Kayıt talebiniz başarıyla alınmıştır. Ödeme bilgileri için 'Ödemelerim' sayfasını kontrol edebilirsiniz.")
        # Şimdilik öğrenci listesine yönlendirelim. Sonra 'Ödemelerim' sayfasını yapacağız.
        return redirect('student_list')
    
    return redirect('cart_detail')

@login_required
def receipt_upload_view(request, enrollment_id):
    # İlgili kaydı getir, eğer yoksa veya başkasına aitse 404 hatası ver
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, parent=request.user)
    
    if request.method == 'POST':
        # Formu hem POST verisi hem de yüklenen dosyalar (FILES) ile doldur
        form = ReceiptUploadForm(request.POST, request.FILES, instance=enrollment)
        if form.is_valid():
            # Formu kaydetmek, dekontu ilgili kayda ekleyecektir
            form.save()
            # Kayıt durumunu manuel olarak güncelle
            enrollment.kayit_durumu = 'ONAY_BEKLENIYOR'
            enrollment.save()
            messages.success(request, 'Dekontunuz başarıyla yüklendi. Onay bekleniyor.')
            return redirect('payment_history')
    
    # Eğer GET isteği ise (veya form geçersizse) bu kısım çalışır ama biz direkt yönlendirme yapacağız.
    return redirect('payment_history')

@login_required
def cart_remove_item_view(request, item_index):
    cart = request.session.get('cart', [])
    
    # Gelen indeksin geçerli bir aralıkta olup olmadığını kontrol et
    if 0 <= item_index < len(cart):
        # Listeden o indeksteki elemanı sil
        del cart[item_index]
        # Session'ı güncellenmiş sepetle kaydet
        request.session['cart'] = cart
        messages.success(request, "Kayıt sepetten kaldırıldı.")
    
    return redirect('cart_detail')

@login_required
def cart_clear_view(request):
    # Session'da 'cart' anahtarı varsa sil
    if 'cart' in request.session:
        del request.session['cart']
        messages.success(request, "Sepetiniz başarıyla boşaltıldı.")
        
    return redirect('home') # Sepet boşaldığı için anasayfaya yönlendir