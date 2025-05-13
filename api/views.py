import logging
from django.urls import reverse
from django.db.models import Count, Avg, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Subcategory, Product, Comment, Cart, CartItem, Composition, CompositionItem
from .serializers import (
    CategorySerializer, SubcategorySerializer, ProductSerializer, 
    CommentSerializer, CartSerializer, CartItemSerializer, CompositionSerializer, CompositionItemSerializer
)

logger = logging.getLogger(__name__)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.filter(subcategories__isnull=False).distinct()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        logger.info(f"Поиск категории с slug: {slug}")
        try:
            category = Category.objects.get(slug=slug)
            logger.info(f"Найдена категория: {category.name} (slug: {category.slug})")
            return category
        except Category.DoesNotExist:
            logger.error(f"Категория с slug {slug} не найдена")
            raise

    @action(detail=True, methods=['get'])
    def get_absolute(self, request, slug=None):
        category = self.get_object()
        url = reverse('category-detail', kwargs={'slug': category.slug})
        return Response({"absolute_url": request.build_absolute_uri(url)})

class SubcategoryViewSet(ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        logger.info(f"Поиск подкатегории с slug: {slug}")
        try:
            subcategory = Subcategory.objects.get(slug=slug)
            logger.info(f"Найдена подкатегория: {subcategory.name} (slug: {subcategory.slug})")
            return subcategory
        except Subcategory.DoesNotExist:
            logger.error(f"Подкатегория с slug {slug} не найдена")
            raise

    @action(detail=True, methods=['get'])
    def get_absolute(self, request, slug=None):
        subcategory = self.get_object()
        url = reverse('subcategory-detail', kwargs={'slug': subcategory.slug})
        return Response({"absolute_url": request.build_absolute_uri(url)})

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['subcategory__category', 'price']

    def get_object(self):
        slug = self.kwargs.get('slug')
        sku = self.kwargs.get('sku')
        logger.info(f"Поиск продукта: slug={slug}, sku={sku}")
        try:
            product = Product.objects.get(slug=slug, sku=sku)
            logger.info(f"Найден продукт: {product.name}")
            return product
        except Product.DoesNotExist:
            logger.error(f"Продукт не найден: slug={slug}, sku={sku}")
            raise

    def get_queryset(self):
        queryset = Product.objects.all()  
        subcategory_slug = self.request.query_params.get('subcategory_slug')
        if subcategory_slug:
            logger.info(f"Фильтр по subcategory_slug: {subcategory_slug}")
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
        logger.info(f"Товаров в queryset: {queryset.count()}")
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        stats = Product.objects.aggregate(
            avg_price=Avg('price'),
            max_price=Max('price'),
            product_count=Count('id')
        )
        return Response(stats)

    @action(detail=True, methods=['get'])
    def get_absolute(self, request, slug=None, sku=None):
        product = self.get_object()
        url = reverse('product-detail', kwargs={'slug': product.slug, 'sku': product.sku})
        return Response({"absolute_url": request.build_absolute_uri(url)})
    
    
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer

class CompositionViewSet(ModelViewSet):
    queryset = Composition.objects.all()
    serializer_class = CompositionSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        logger.info(f"Поиск композиции с slug: {slug}")
        try:
            composition = Composition.objects.get(slug=slug)
            logger.info(f"Найдена композиция: {composition.name} (slug: {composition.slug})")
            return composition
        except Composition.DoesNotExist:
            logger.error(f"Композиция с slug {slug} не найдена")
            raise

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer