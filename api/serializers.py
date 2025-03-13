from rest_framework import serializers
from .models import (
    Category, Subcategory, Product, Comment, 
    Attribute, ProductAttribute, Cart, CartItem, 
    Composition, CompositionItem
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Subcategory
        fields = '__all__'

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
