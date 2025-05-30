from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Product

def generate_products_pdf(queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products.pdf"'
    p = canvas.Canvas(response)
    y = 800
    p.setFont("Helvetica", 12)
    p.drawString(100, y, "Список товаров:")
    y -= 30
    for product in queryset:
        line = f"{product.name} | SKU: {product.sku} | Цена: {product.price} | Остаток: {product.stock}"
        p.drawString(100, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
    p.save()
    return response
