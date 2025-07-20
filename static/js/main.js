// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- ÖĞRENCİ SEÇİM MODALI İÇİN KODLAR (ANASAYFA) ---
    const studentSelectModal = document.getElementById('student-select-modal');
    // Bu kontrol, sadece anasayfada (bu modalın olduğu yerde) çalışmasını sağlar
    if (studentSelectModal) {
        const closeModalBtn = studentSelectModal.querySelector('.modal-close');
        const openModalBtns = document.querySelectorAll('.btn-open-modal');
        const studentSelect = document.getElementById('modal-student-select');
        const modalCourseIdInput = document.getElementById('modal-course-id');
        const addToCartForm = document.getElementById('add-to-cart-form');

        openModalBtns.forEach(button => {
            button.addEventListener('click', function() {
                // 1. Adım: Kullanıcının giriş durumunu HTML'den oku
                const isAuthenticated = document.body.dataset.isAuthenticated === 'true';

                // 2. Adım: Kontrol et
                if (isAuthenticated) {
                    // EĞER GİRİŞ YAPMIŞSA: ESKİ KODU ÇALIŞTIR (Öğrenci seçim penceresini aç)
                    const courseId = this.dataset.courseId;
                    modalCourseIdInput.value = courseId;
                    fetch('/hesap/api/get-students/')
                        .then(response => response.json())
                        .then(data => {
                            studentSelect.innerHTML = '<option value="">Öğrenci Seçiniz...</option>';
                            if (data.students.length > 0) {
                                data.students.forEach(student => {
                                    const option = document.createElement('option');
                                    option.value = student.id;
                                    option.textContent = student.name;
                                    studentSelect.appendChild(option);
                                });
                            } else {
                                studentSelect.innerHTML = '<option value="">Panele kayıtlı öğrenciniz yok</option>';
                            }
                            studentSelectModal.style.display = 'flex';
                        });
                } else {
                    // EĞER GİRİŞ YAPMAMIŞSA: YENİ UYARI PENCERESİNİ GÖSTER
                    const loginRequiredModal = document.getElementById('login-required-modal');
                    if (loginRequiredModal) {
                        loginRequiredModal.style.display = 'flex';
                    }
                }
            });
        });

        closeModalBtn.addEventListener('click', () => {
            studentSelectModal.style.display = 'none';
        });
        window.addEventListener('click', (event) => {
            if (event.target == studentSelectModal) {
                studentSelectModal.style.display = 'none';
            }
        });

        addToCartForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(this);
            fetch('/sepet/ekle/', {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    studentSelectModal.style.display = 'none';
                    document.getElementById('cart-count').textContent = data.cart_item_count;
                } else {
                    alert('Hata: ' + data.message);
                }
            });
        });
    }
    // --- GİRİŞ GEREKLİ MODALI İŞLEVLERİ ---
    const loginRequiredModal = document.getElementById('login-required-modal');
    if (loginRequiredModal) {
        const closeBtn = loginRequiredModal.querySelector('.login-required-modal-close');
        closeBtn.addEventListener('click', () => {
            loginRequiredModal.style.display = 'none';
        });
    }

    // --- DEKONT YÜKLEME MODALI İÇİN KODLAR (ÖDEMELERİM SAYFASI) ---
    const receiptUploadModal = document.getElementById('receipt-upload-modal');
    // Bu kontrol, sadece "Ödemelerim" sayfasında (bu modalın olduğu yerde) çalışmasını sağlar
    if (receiptUploadModal) {
        const openReceiptModalBtns = document.querySelectorAll('.btn-open-receipt-modal');
        const receiptModalCloseBtn = receiptUploadModal.querySelector('.receipt-modal-close');
        const receiptUploadForm = document.getElementById('receipt-upload-form');

        openReceiptModalBtns.forEach(button => {
            button.addEventListener('click', function() {
                const enrollmentId = this.dataset.enrollmentId;
                // Formun action adresini doğru ID ile dinamik olarak güncelle
                receiptUploadForm.action = `/sepet/dekont-yukle/${enrollmentId}/`;
                receiptUploadModal.style.display = 'flex';
            });
        });

        receiptModalCloseBtn.addEventListener('click', () => {
            receiptUploadModal.style.display = 'none';
        });
         window.addEventListener('click', (event) => {
            if (event.target == receiptUploadModal) {
                receiptUploadModal.style.display = 'none';
            }
        });
    }

    // --- AKORDİYON MENÜ İŞLEVLERİ (ANASAYFA) ---
    const accordionHeaders = document.querySelectorAll('.accordion-header');
    if(accordionHeaders.length > 0) {
        // İlk elemanı başlangıçta açık yap
        let firstContent = accordionHeaders[0].nextElementSibling;
        if(firstContent) {
            accordionHeaders[0].classList.add('active');
            firstContent.style.maxHeight = firstContent.scrollHeight + "px";
        }
        
        accordionHeaders.forEach(header => {
            header.addEventListener('click', function() {
                this.classList.toggle('active');
                let content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        });
    }

    // --- "NASIL KAYIT OLURUM" MODALI İŞLEVLERİ (ANASAYFA) ---
    const howToRegisterModal = document.getElementById('how-to-register-modal');
    if (howToRegisterModal) {
        const openBtn = document.getElementById('how-to-register-btn');
        const closeBtns = document.querySelectorAll('.how-to-register-modal-close');

        openBtn.addEventListener('click', () => {
            howToRegisterModal.style.display = 'flex';
        });

        closeBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                howToRegisterModal.style.display = 'none';
            });
        });
    }

    

});