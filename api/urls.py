from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CommentViewSet, CompositionViewSet, CategoryViewSet, SubcategoryViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import HighRatingProductsView, SearchProductsView, UpdateProductPriceView, DeleteProductView
from .views import PromotionViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'compositions', CompositionViewSet, basename='composition')
router.register(r'promotions', PromotionViewSet, basename='promotion')


category_list = CategoryViewSet.as_view({'get': 'list'})
category_detail = CategoryViewSet.as_view({'get': 'retrieve'})
subcategory_detail = SubcategoryViewSet.as_view({'get': 'retrieve'})
product_list = ProductViewSet.as_view({'get': 'list'})
product_detail = ProductViewSet.as_view({'get': 'retrieve'})
composition_detail = CompositionViewSet.as_view({'get': 'retrieve'})
comment_list = CommentViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('', include(router.urls)),
    path('categories/', category_list, name='category-list'),
    path('category/<slug:slug>/', category_detail, name='category-detail'),
    path('subcategory/<slug:slug>/', subcategory_detail, name='subcategory-detail'),
    path('subcategory/<slug:subcategory_slug>/<slug:slug>/<str:sku>/', product_detail, name='product-detail'),
    path('products/', product_list, name='product-list'),
    path('products/<slug:slug>/<str:sku>/', product_detail, name='product-detail'),
    path('composition/<slug:slug>/', composition_detail, name='composition-detail'),
    path('comments/', comment_list, name='comment-list'),
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('products/high-rating/', HighRatingProductsView.as_view(), name='high_rating_products'),
    path('products/search/', SearchProductsView.as_view(), name='search_products'),
    path('products/update-price/', UpdateProductPriceView.as_view(), name='update_product_price'),
    path('products/delete/', DeleteProductView.as_view(), name='delete_product'),
] + router.urls