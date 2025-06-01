from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import User
from django.db.models import Avg
from pytils.translit import slugify as ru_slugify
from backend import settings

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ru_slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Subcategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    
    def __str__(self):
        return f"{self.category.name} -> {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ru_slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'

class ProductManager(models.Manager):
    def with_high_rating(self):
        return self.annotate(avg_rating=Avg('comments__rating')).filter(avg_rating__gte=4)

    def search_by_name(self, query):
        return self.filter(name__icontains=query)  

    def get_values(self):
        return self.values('name', 'price')  

    def get_values_list(self):
        return self.values_list('name', flat=True)  

    def count_products(self):
        return self.count() 

    def exists_product(self, name):
        return self.filter(name=name).exists()  

    def update_price(self, name, new_price):
        return self.filter(name=name).update(price=new_price)  

    def delete_by_name(self, name):
        return self.filter(name=name).delete() 

class Product(models.Model):
    name = models.CharField(max_length=255)
    attributes = models.ManyToManyField(
        'Attribute',
        through='ProductAttribute',
        related_name='products'
    )
    slug = models.SlugField(max_length=255, blank=True)
    sku = models.CharField(max_length=50, unique=True, verbose_name='Артикул', default='000000')
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True, default=None)
    instruction_document = models.FileField(upload_to='product_instructions/', null=True, blank=True, default=None)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=200, blank=True, null=True, verbose_name="URL")  # Добавлено поле URLField

    objects = ProductManager()

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = ru_slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug, sku=self.sku).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Пользователь')  # Используем кастомную модель
    text = models.TextField(verbose_name='Текст комментария')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='comments', verbose_name='Продукт')
    rating = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')), default=3, verbose_name='Рейтинг')
    created_at = models.DateTimeField(verbose_name='Дата создания', default=timezone.now)
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
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_attributes'  # Изменено related_name
    )
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, default='N/A')
    
    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"
    
    class Meta:
        verbose_name = 'Атрибут продукта'
        verbose_name_plural = 'Атрибуты продуктов'
        unique_together = ('product', 'attribute')

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    designer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='compositions')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="composition_images/", null=True, blank=True, default=None)

    def __str__(self):
        return f"Композиция {self.name} от {self.designer.get_full_name() or self.designer.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = ru_slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('composition-detail', kwargs={'slug': self.slug})

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