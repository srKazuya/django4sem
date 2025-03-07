from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from filer.fields.image import FilerImageField

from backend import settings
from users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return f"{self.category.name} -> {self.name}"
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

class Product(models.Model):
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул', default='000000')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)  
    image = FilerImageField(on_delete=models.CASCADE, related_name="product_images", null=True, blank=True, default=None)
    description = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE,related_name='comments', verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст комментария')
    product = models.ForeignKey('Product', on_delete=models.CASCADE,related_name='comments',verbose_name='Продукт')
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')), default=3, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', default=timezone.now)
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    
    def __str__(self):
        return f"Комментарий от {self.user} к {self.product.name}"
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at'] 
class Attribute(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, default='N/A')
    
    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
    
    class Meta:
        verbose_name = 'Атрибут продукта'
        verbose_name_plural = 'Атрибуты продуктов'
        unique_together = ('product', 'attribute')  


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    
    def __str__(self):
        return f"Корзина {self.user.email if self.user else 'Анонимного пользователя'}"
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
    
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

class Composition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    designer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compositions')
    created_at = models.DateTimeField(auto_now_add=True)
    image = FilerImageField(on_delete=models.CASCADE, related_name="composition_images", null=True, blank=True, default=None)
    
    def __str__(self):
        return f"Композиция {self.name} от {self.designer.first_name}"
    
    class Meta:
        verbose_name = 'Композиция'
        verbose_name_plural = 'Композиции'

class CompositionItem(models.Model):
    composition = models.ForeignKey(Composition, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.product.name} в {self.composition.name}"
    
    class Meta:
        verbose_name = 'Товар в композиции'
        verbose_name_plural = 'Товары в композиции'
