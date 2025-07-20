# enrollments/context_processors.py (Yeni oluşturulan dosya)

def cart_context_processor(request):
    """
    Her şablona sepetin içindeki ürün sayısını gönderen fonksiyon.
    """
    # Session'dan sepeti al, eğer sepet yoksa boş bir liste döner.
    cart = request.session.get('cart', [])
    cart_item_count = len(cart)
    # Bu sözlüğü, tüm şablonların context'ine ekler.
    return {'cart_item_count': cart_item_count}