from django.contrib import admin
from .models import Category, Product, Attribute, ProductAttribute, Customer, Order, OrderItem, Cart, CartItem

# Inline для OrderItem в OrderAdmin
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    raw_id_fields = ("product",)

# Inline для CartItem в CartAdmin
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    raw_id_fields = ("product",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent")
    list_filter = ("parent",)
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "get_attributes")
    list_filter = ("category", "price")
    search_fields = ("name", "description")
    raw_id_fields = ("category",)
    
    @admin.display(description="Атрибуты")
    def get_attributes(self, obj):
        return ", ".join([f"{pa.attribute.name}: {pa.value}" for pa in obj.attributes.all()])

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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "created_at", "total_price")
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    search_fields = ("customer__email",)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "price")
    list_filter = ("order", "product")
    raw_id_fields = ("order", "product")

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
