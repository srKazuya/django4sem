from django.urls import reverse
from rest_framework import serializers
from .models import (
    Category, Subcategory, Product, Comment, 
    Attribute, ProductAttribute, Cart, CartItem, 
    Composition, CompositionItem
)
from django.contrib.auth.models import User

class SubcategoryShortSerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'absolute_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('subcategory-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)

class SubcategorySerializer(serializers.ModelSerializer):
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'absolute_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('subcategory-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategoryShortSerializer(many=True, read_only=True)
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'subcategories', 'absolute_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('category-detail', kwargs={'slug': obj.slug})
        return request.build_absolute_uri(url)

class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubcategoryShortSerializer(read_only=True)
    absolute_url = serializers.SerializerMethodField()
    image = serializers.ImageField(required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'sku', 'subcategory', 'price', 'stock', 'image', 'description', 'absolute_url')

    def get_absolute_url(self, obj):
        request = self.context.get('request')
        if not request:
            return None
        url = reverse('product-detail', kwargs={'slug': obj.slug, 'sku': obj.sku})
        return request.build_absolute_uri(url)

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
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Composition
        fields = ('id', 'name', 'slug', 'designer', 'created_at', 'image', 'absolute_url')

    def get_absolute_url(self, obj):
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
        
        
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password']
#         )
#         return user