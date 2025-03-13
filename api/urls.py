from django.urls import path, include
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet,  CommentViewSet


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
