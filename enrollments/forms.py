# enrollments/forms.py (Yeni oluşturulan dosya)
from django import forms
from .models import Enrollment

class ReceiptUploadForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        # Formda sadece 'dekont' alanını göster
        fields = ['dekont']