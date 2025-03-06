from django.contrib import admin
from .models import (
    Category, Subcategory, Product, Attribute, ProductAttribute, Customer,
    Cart, CartItem, Composition, CompositionItem
)

# Inline для CartItem в CartAdmin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    raw_id_fields = ("product",)

# Inline для CompositionItem в CompositionAdmin 
class CompositionItemInline(admin.TabularInline):
    model = CompositionItem
    extra = 1
    raw_id_fields = ("product",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "subcategory", "price", "stock", "get_image")
    list_filter = ("subcategory", "price")
    search_fields = ("name", "sku", "description")
    raw_id_fields = ("subcategory",)
    
    @admin.display(description="Изображение")
    def get_image(self, obj):
        return obj.image.url if obj.image else "Нет изображения"


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ("product", "attribute", "value")
    list_filter = ("attribute",)
    search_fields = ("product__name", "attribute__name", "value")

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at")
    date_hierarchy = "created_at"
    search_fields = ("customer__email",)
    inlines = [CartItemInline]

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("cart", "product", "quantity")
    list_filter = ("cart", "product")
    raw_id_fields = ("cart", "product")

@admin.register(Composition)
class CompositionAdmin(admin.ModelAdmin):
    list_display = ("name", "designer", "created_at", "get_image")
    date_hierarchy = "created_at"
    search_fields = ("name", "designer__email")
    inlines = [CompositionItemInline]
    
    @admin.display(description="Изображение")
    def get_image(self, obj):
        return obj.image.url if obj.image else "Нет изображения"


@admin.register(CompositionItem)
class CompositionItemAdmin(admin.ModelAdmin):
    list_display = ("composition", "product", "quantity")
    list_filter = ("composition", "product")
    raw_id_fields = ("composition", "product")
