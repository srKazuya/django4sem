from django.urls import reverse
from pytils.translit import slugify as ru_slugify
from rest_framework import serializers
from .models import (
    Category, Subcategory, Product, Comment, 
    Attribute, ProductAttribute, Cart, CartItem, 
    Composition, CompositionItem
)

class SubcategoryShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name')
class SubcategorySerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'absolute_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None  # Или обработайте ошибку иначе
        slug_name = ru_slugify(obj.name)
        url = reverse('subcategory-detail', kwargs={'slug': slug_name})
        return request.build_absolute_uri(url)
class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()  # Добавляем для категорий

    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories', 'absolute_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        slug_name = ru_slugify(obj.name)
        url = reverse('category-detail', kwargs={'slug': slug_name})
        return request.build_absolute_uri(url)



class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(read_only=True)
    image = serializers.ImageField(required=False)  

    class Meta:
        model = Product
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True) 
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

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

class CartSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = '__all__'

class CompositionSerializer(serializers.ModelSerializer):
    designer = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Composition
        fields = '__all__'

class CompositionItemSerializer(serializers.ModelSerializer):
    composition = CompositionSerializer(read_only=True)
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CompositionItem
        fields = '__all__'
