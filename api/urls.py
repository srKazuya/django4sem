from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,  CommentViewSet, CompositionViewSet, CategoryViewSet, SubcategoryViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'comments', CommentViewSet, basename='comment')


category_list = CategoryViewSet.as_view({'get': 'list'})
category_detail = CategoryViewSet.as_view({'get': 'retrieve'})
subcategory_detail = SubcategoryViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
    path('', include(router.urls)),
    
    path('subcategory/<slug:slug>/', SubcategoryViewSet.as_view({'get': 'retrieve'}), name='subcategory-detail'),
    path('category/<slug:slug>/', SubcategoryViewSet.as_view({'get': 'retrieve'}), name='category-detail'),
    path('products/<slug:name>/<str:sku>/', ProductViewSet.as_view({'get': 'retrieve'}), name='product-detail'),
]
