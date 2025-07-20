# accounts/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm
from django.http import JsonResponse
from enrollments.models import Enrollment 
from .forms import UserUpdateForm
from django.contrib.auth import login
from main.models import Course

def register_view(request):
    # Giriş yapmış kullanıcı bu sayfayı göremez
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        student_form = StudentForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            # 1. Veli (User) hesabını kaydet
            yeni_veli = user_form.save()

            # 2. Öğrenciyi veliye bağlayarak kaydet
            yeni_ogrenci = student_form.save(commit=False)
            yeni_ogrenci.parent = yeni_veli
            yeni_ogrenci.save()

            # --- YENİ EKLENEN OTOMATİK SEPETE EKLEME BÖLÜMÜ ---
            try:
                # Sitedeki aktif olan ilk kursu bul
                ilgilenilen_kurs = Course.objects.filter(program__is_active=True).first()
                if ilgilenilen_kurs:
                    # Sepeti session'dan al veya boş bir liste oluştur
                    cart = request.session.get('cart', [])
                    
                    # Yeni kaydı sepete ekle
                    cart.append({
                        'course_id': str(ilgilenilen_kurs.id),
                        'student_id': str(yeni_ogrenci.id)
                    })
                    # Session'ı güncelle
                    request.session['cart'] = cart
            except:
                # Eğer kurs bulunamazsa veya bir hata olursa, sürece devam et ama sepete ekleme
                pass
            # --- BÖLÜM SONU ---
            
            # 3. Kullanıcıyı otomatik olarak giriş yaptır
            login(request, yeni_veli)
            
            messages.success(request, 'Hesabınız ve ilk öğrenciniz başarıyla oluşturuldu. Eğitim programı sepetinize eklendi!')
            
            # 4. Kullanıcıyı artık doğrudan SEPETE yönlendir!
            return redirect('cart_detail')
    else:
        user_form = CustomUserCreationForm()
        student_form = StudentForm()

    context = {
        'user_form': user_form,
        'student_form': student_form
    }
    return render(request, 'accounts/register.html', context)

@login_required # Bu satır, bu view'ın çalışmadan önce kullanıcının giriş yapmış olmasını zorunlu kılar.
def student_list_view(request):
    # Veritabanından, parent'ı (velisi) şu anki giriş yapmış kullanıcı olan öğrencileri filtrele
    students = Student.objects.filter(parent=request.user)
    
    context = {
        'students': students
    }
    return render(request, 'accounts/student_list.html', context)

@login_required
def student_add_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            # Formu hemen kaydetme, çünkü 'parent' alanı eksik
            student = form.save(commit=False)
            # Eksik olan parent alanını, o an giriş yapmış kullanıcı olarak ata
            student.parent = request.user
            # Şimdi tüm alanlar dolu, öğrenciyi veritabanına kaydet
            student.save()
            messages.success(request, f"{student.first_name} başarıyla eklendi.")
            return redirect('student_list') # Öğrenci listesine geri yönlendir
    else:
        form = StudentForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/student_form.html', context)

@login_required
def get_students_json_view(request):
    students = Student.objects.filter(parent=request.user)
    # Öğrenci listesini JSON formatına uygun bir yapıya dönüştürüyoruz
    student_list = [{'id': student.id, 'name': f"{student.first_name} {student.last_name}"} for student in students]
    return JsonResponse({'students': student_list})

@login_required
def payment_history_view(request):
    # parent'ı (velisi) şu anki giriş yapmış kullanıcı olan tüm kayıtları
    # oluşturulma tarihine göre en yeniden eskiye doğru sırala
    enrollments = Enrollment.objects.filter(parent=request.user).order_by('-created_at')

    context = {
        'enrollments': enrollments
    }
    return render(request, 'accounts/payment_list.html', context)

@login_required
def profile_update_view(request):
    if request.method == 'POST':
        # Formu, hem gelen yeni veriyle hem de mevcut kullanıcı bilgileriyle doldur
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bilgileriniz başarıyla güncellendi.')
            return redirect('profile_update') # Aynı sayfaya geri yönlendir
    else:
        # Sayfa ilk açıldığında, formu mevcut kullanıcı bilgileriyle doldur
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/profile_update_form.html', context)