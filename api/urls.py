from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,  CommentViewSet, CompositionViewSet, CategoryViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api/products/<slug:name>/<str:sku>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
]
