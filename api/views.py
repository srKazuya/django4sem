# from django.db.models import Count, Avg, Max
# from django.urls import reverse
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from api import models

# from .models import (
#     Category, Subcategory, Product, Comment, 
#     Attribute, ProductAttribute, Cart, CartItem, 
#     Composition, CompositionItem
# )
# from .serializers import (
#     CategorySerializer, SubcategorySerializer, ProductSerializer, 
#     CommentSerializer, AttributeSerializer, ProductAttributeSerializer, 
#     CartSerializer, CartItemSerializer, CompositionSerializer, CompositionItemSerializer
# )
# from api import models



# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['subcategory__category', 'price']  # 6. Использование __ (обращение к связанной таблице)
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         queryset = queryset.filter(stock__gt=0)  # 5. Метод filter()
#         queryset = queryset.exclude(price=0)  # 7. Метод exclude()
#         queryset = queryset.order_by('-price')  # 8. Метод order_by()
#         return queryset

#     # 11. Функции агрегирования и аннотирования (три примера)
#     @action(detail=False, methods=['get'])
#     def stats(self, request):
#         stats = Product.objects.aggregate(
#             avg_price=Avg('price'),  # Средняя цена товаров
#             max_price=Max('price'),  # Максимальная цена
#             product_count=Count('id')  # Количество товаров
#         )
#         return Response(stats)

# class CommentViewSet(ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

# class CompositionViewSet(ModelViewSet):
#     queryset = Composition.objects.all()
#     serializer_class = CompositionSerializer

#     # 10. get_absolute_url, reverse
#     @action(detail=True, methods=['get'])
#     def get_absolute(self, request, pk=None):
#         composition = self.get_object()
#         url = reverse('composition-detail', kwargs={'pk': composition.pk})
#         return Response({"absolute_url": request.build_absolute_uri(url)})

# class CartViewSet(ModelViewSet):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

# class CartItemViewSet(ModelViewSet):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer\
from django.utils.text import slugify
from pytils.translit import slugify as ru_slugify
from django.db.models import Count, Avg, Max
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Subcategory, Product, Comment, Cart, CartItem, Composition
from .serializers import (
    CategorySerializer, SubcategorySerializer, ProductSerializer, 
    CommentSerializer, CartSerializer, CartItemSerializer, CompositionSerializer
)



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.with_high_rating()  
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory__category', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(stock__gt=0)
        queryset = queryset.exclude(price=0)
        queryset = queryset.order_by('-price')
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Функция агрегации: средняя цена, макс. цена, кол-во товаров"""
        stats = Product.objects.aggregate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            product_count=Count('id')
        )
        return Response(stats)

    @action(detail=False, methods=['get'], url_path='high-rating')
    def high_rating(self, request):
        """Фильтруем товары с высоким рейтингом (avg_rating >= 4)"""
        high_rating_products = Product.objects.with_high_rating()
        serializer = self.get_serializer(high_rating_products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_absolute(self, request, pk=None):
        product = self.get_object()
        if not product.name:
            return Response({"error": "Product name is empty"}, status=400)
        slug_name = ru_slugify(product.name)  
        url = reverse('product-detail', kwargs={'name': slug_name, 'sku': product.sku})
        return Response({"absolute_url": request.build_absolute_uri(url)})
    
    queryset = Product.objects.with_high_rating()  
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory__category', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(stock__gt=0)
        queryset = queryset.exclude(price=0)
        queryset = queryset.order_by('-price')
        return queryset

    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = Product.objects.aggregate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            product_count=Count('id')
        )
        return Response(stats)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CompositionViewSet(ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer

    @action(detail=True, methods=['get'])
    def get_absolute(self, request, pk=None):
        composition = self.get_object()
        return Response({"absolute_url": request.build_absolute_uri(composition.get_absolute_url())})

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
