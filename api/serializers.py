from django.urls import reverse
from rest_framework import serializers
from .models import (
    Category, Order, OrderItem, Subcategory, Product, Comment, 
    Attribute, ProductAttribute, Cart, CartItem, 
    Composition, CompositionItem, Promotion
)
from users.models import User
from typing import Any, Dict, Optional

class SubcategoryShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор для подкатегории с краткой информацией.
    """
    absolute_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'absolute_url', 'category_name')

    def get_absolute_url(self, obj: Subcategory) -> Optional[str]:
        """
        Получить абсолютный URL для подкатегории.

        Аргументы:
            obj (Subcategory): Экземпляр подкатегории.

        Возвращает:
            Optional[str]: Абсолютный URL или None, если запрос недоступен.
        """
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('subcategory-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)

class SubcategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для подкатегории с полной информацией.
    """
    absolute_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    note = serializers.SerializerMethodField()
    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'absolute_url', 'category_name', 'note')

    def get_absolute_url(self, obj: Subcategory) -> Optional[str]:
        """
        Получить абсолютный URL для подкатегории.

        Аргументы:
            obj (Subcategory): Экземпляр подкатегории.

        Возвращает:
            Optional[str]: Абсолютный URL или None, если запрос недоступен.
        """
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('subcategory-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)
    def get_note(self, obj: Category) -> Optional[str]:

        return self.context.get('custom_note')

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категории с подкатегориями.
    """
    subcategories = SubcategoryShortSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()
    note = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories', 'absolute_url', 'note')

    def get_absolute_url(self, obj: Category) -> Optional[str]:
        """
        Получить абсолютный URL для категории.

        Аргументы:
            obj (Category): Экземпляр категории.

        Возвращает:
            Optional[str]: Абсолютный URL или None, если запрос недоступен.
        """
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('category-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)
    
    def get_note(self, obj: Category) -> Optional[str]:

        return self.context.get('custom_note')
    
class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продукта с деталями.
    """
    subcategory = SubcategoryShortSerializer(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'sku', 'subcategory', 'price', 'stock', 'image', 'description', 'absolute_url')

    def get_absolute_url(self, obj: Product) -> Optional[str]:
        """
        Получить абсолютный URL для продукта.

        Аргументы:
            obj (Product): Экземпляр продукта.

        Возвращает:
            Optional[str]: Абсолютный URL или None, если запрос недоступен.
        """
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('subcategory-detail', kwargs={'slug': obj.subcategory.slug})
        product_url = f"{url}{obj.slug}/{obj.sku}/"
        return request.build_absolute_uri(product_url)

class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элемента корзины с деталями продукта.
    """
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    cart = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_id', 'quantity']

    # def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
    #     """
    #     Валидировать данные элемента корзины.

    #     Аргументы:
    #         data (Dict[str, Any]): Данные для валидации.

    #     Возвращает:
    #         Dict[str, Any]: Проверенные данные.

    #     Вызывает:
    #         serializers.ValidationError: Если запрашиваемое количество превышает наличие на складе.
    #     """
    #     product = data.get('product')
    #     quantity = data.get('quantity')

    #     if not product:
    #         raise serializers.ValidationError("Продукт не найден.")

    #     if product.stock < quantity:
    #         raise serializers.ValidationError({
    #             'quantity': f'На складе доступно только {product.stock} шт.'
    #         })

    # return data

class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для корзины с ее элементами.
    """
    user = serializers.CharField(source='user.username', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']

    def get_total_price(self, obj: Cart) -> float:
        """
        Рассчитать общую стоимость корзины.

        Аргументы:
            obj (Cart): Экземпляр корзины.

        Возвращает:
            float: Общая стоимость корзины.
        """
        return sum(item.product.price * item.quantity for item in obj.items.all())

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    userId = serializers.IntegerField(source='user.id', read_only=True)  # Добавляем userId
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  

    class Meta:
        model = Comment
        fields = ['id', 'user', 'userId', 'product', 'text', 'rating', 'created_at', 'is_approved']
        read_only_fields = ['id', 'user', 'userId', 'created_at', 'is_approved']
        
class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    attribute = AttributeSerializer(read_only=True)

    class Meta:
        model = ProductAttribute
        fields = '__all__'

class CompositionSerializer(serializers.ModelSerializer):
    designer = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(required=False)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Composition
        fields = ('id', 'name', 'slug', 'designer', 'created_at', 'image', 'absolute_url')

    def get_absolute_url(self, obj):
        """
        Получить абсолютный URL для композиции.

        Аргументы:
            obj (Composition): Экземпляр композиции.

        Возвращает:
            Optional[str]: Абсолютный URL или None, если запрос недоступен.
        """
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('composition-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)

class CompositionItemSerializer(serializers.ModelSerializer):
    composition = CompositionSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CompositionItem
        fields = '__all__'
        
class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'
        
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'created_at', 'total_price', 'items']
        read_only_fields = ['user', 'created_at', 'total_price']

    # def validate_address(self, value: str) -> str:
    #     """
    #     Проверка адреса доставки.

    #     Аргументы:
    #         value (str): Адрес доставки.

    #     Возвращает:
    #         str: Проверенный адрес.

    #     Вызывает:
    #         serializers.ValidationError: Если адрес некорректен.
    #     """
    #     if len(value.strip()) < 3:
    #         raise serializers.ValidationError("Адрес должен содержать минимум 3 символа.")
    #     return value

    # def validate(self, data):
    #     """
    #     Общая валидация данных заказа.

    #     Аргументы:
    #         data (Dict[str, Any]): Данные заказа.

    #     Возвращает:
    #         Dict[str, Any]: Проверенные данные заказа.

    #     Вызывает:
    #         serializers.ValidationError: Если данные заказа некорректны.
    #     """
    #     total_price = data.get('total_price')
    #     if total_price is not None:
    #         if total_price < 500:
    #             raise serializers.ValidationError("Сумма заказа должна быть не меньше 500 рублей.")
    #         if total_price > 1_000_000:
    #             raise serializers.ValidationError("Сумма заказа не может превышать 1 000 000 рублей.")
        # return data
