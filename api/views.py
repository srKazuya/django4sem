import logging
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db.models import Avg, Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.db.models import Count, Avg, Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from api.filters import ProductFilter
from .models import Category, Order, OrderItem, Subcategory, Product, Comment, Cart, CartItem, Composition, CompositionItem, Promotion
from .serializers import (
    CategorySerializer, OrderSerializer, SubcategorySerializer, ProductSerializer, 
    CommentSerializer, CartSerializer, CartItemSerializer, CompositionSerializer, CompositionItemSerializer, PromotionSerializer
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
    queryset = Product.objects.select_related('subcategory').prefetch_related('attributes').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
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

        queryset = queryset.annotate(
            avg_rating=Avg('comments__rating'),
            total_stock=Sum('stock'),
            max_price=Max('price')
        )

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
    
    @action(detail=False, methods=['get'])
    def high_rating(self, request):
        products = Product.objects.with_high_rating()
        if not products.exists():
            return Response({"message": "No products with high rating found."}, status=status.HTTP_404_NOT_FOUND)
        data = []
        for product in products:
            try:
                data.append({
                    "image": request.build_absolute_uri(product.image.url) if product.image else None,
                    "name": product.name,
                    "price": product.price,
                    "rating": product.comments.aggregate(avg_rating=Avg('rating'))['avg_rating'],
                    "absolute_url": request.build_absolute_uri(reverse('product-detail', kwargs={"slug": product.slug, "sku": product.sku})),
                    "subcategory": {"slug": product.subcategory.slug if product.subcategory else "undefined"},
                    "slug": product.slug if product.slug else "undefined",
                    "sku": product.sku if product.sku else "undefined"
                })
            except UnicodeDecodeError as e:
                logger.error(f"Encoding error for product {product.id}: {e}")
                data.append({
                    "image": None,
                    "name": "Encoding Error",
                    "price": "N/A",
                    "rating": None,
                    "absolute_url": None,
                    "subcategory": {"slug": "undefined"},
                    "slug": "undefined",
                    "sku": "undefined"
                })
        return Response(data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        products = Product.objects.search_by_name(query)
        data = [
            {
                "name": product.name,
                "price": product.price
            }
            for product in products
        ]
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def values(self, request):
        data = Product.objects.get_values()
        return Response(data)

    @action(detail=False, methods=['get'])
    def values_list(self, request):
        data = Product.objects.get_values_list()
        return Response(data)

    @action(detail=False, methods=['get'])
    def count(self, request):
        count = Product.objects.count_products()
        return Response({"count": count})

    @action(detail=False, methods=['get'])
    def exists(self, request):
        name = request.query_params.get('name', '')
        exists = Product.objects.exists_product(name)
        return Response({"exists": exists})

    @action(detail=False, methods=['patch'])
    def update_price(self, request):
        name = request.data.get('name')
        new_price = request.data.get('new_price')
        updated = Product.objects.update_price(name, new_price)
        return Response({"updated": updated})

    @action(detail=False, methods=['delete'])
    def delete(self, request):
        name = request.data.get('name')
        deleted, _ = Product.objects.delete_by_name(name)
        return Response({"deleted": deleted})

    @action(detail=False, methods=['get'])
    def new_products(self, request):
        from datetime import timedelta
        from django.utils.timezone import now

        one_week_ago = now() - timedelta(days=7)
        products = Product.objects.filter(created_at__gte=one_week_ago)

        if not products.exists():
            return Response({"message": "No new products found."}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                "image": request.build_absolute_uri(product.image.url) if product.image else None,
                "name": product.name,
                "price": product.price,
                "rating": product.comments.aggregate(avg_rating=Avg('rating'))['avg_rating'],
                "absolute_url": request.build_absolute_uri(reverse('product-detail', kwargs={"slug": product.slug, "sku": product.sku})),
                "subcategory": {"slug": product.subcategory.slug if product.subcategory else "undefined"},
                "slug": product.slug if product.slug else "undefined",
                "sku": product.sku if product.sku else "undefined"
            }
            for product in products
        ]

        return Response(data, status=status.HTTP_200_OK)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all() 
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  

    def get_queryset(self):
        product_id = self.request.query_params.get('product')
        if product_id:
            return self.queryset.filter(product_id=product_id)
        return self.queryset

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


class CartDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            cart = Cart.objects.prefetch_related('items__product').get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddCartItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
        
class UpdateCartItemView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
class RemoveCartItemView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(cart__user=self.request.user)
    
class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class HighRatingProductsView(APIView):
    def get(self, request):
        products = Product.objects.with_high_rating()
        data = [
            {
                "name": product.name,
                "price": product.price,
                "rating": product.comments.aggregate(avg_rating=Avg('rating'))['avg_rating']
            }
            for product in products
        ]
        return Response(data, status=status.HTTP_200_OK)

class SearchProductsView(APIView):
    def get(self, request):
        query = request.query_params.get('query', '')
        products = Product.objects.search_by_name(query)
        data = [
            {
                "name": product.name,
                "price": product.price
            }
            for product in products
        ]
        return Response(data, status=status.HTTP_200_OK)

class UpdateProductPriceView(APIView):
    def patch(self, request):
        name = request.data.get('name')
        new_price = request.data.get('new_price')
        if not name or not new_price:
            return Response({"error": "Name and new_price are required"}, status=status.HTTP_400_BAD_REQUEST)
        updated = Product.objects.update_price(name, new_price)
        if updated:
            return Response({"message": "Price updated successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteProductView(APIView):
    def delete(self, request):
        name = request.data.get('name')
        if not name:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        deleted, _ = Product.objects.delete_by_name(name)
        if deleted:
            return Response({"message": "Product deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class PromotionViewSet(ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        address = request.data.get('address')
        try:
            cart = Cart.objects.prefetch_related('items__product').get(user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        if not cart.items.exists():
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=user, address=address, total_price=total_price)

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)