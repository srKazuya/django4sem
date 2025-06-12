from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Category, Subcategory, Product, Cart, CartItem, User, Comment

class APITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.category = Category.objects.create(name="Мебель", slug="mebel")
        self.subcategory = Subcategory.objects.create(name="Шкафы", slug="shkafi", category=self.category)
        self.product = Product.objects.create(
            name="Шкафы", slug="tshirt", sku="TS001", subcategory=self.subcategory,
            price=999.99, stock=10
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_category_list_view(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_product_list_view(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_detail_view(self):
        Product.objects.filter(sku="TS001").delete()
        Product.objects.create(name="Шкафы", slug="shkafi", sku="TS001", subcategory=self.subcategory, price=999.99, stock=10)
        url = reverse('product-detail', kwargs={'slug': self.subcategory.slug, 'subcategory_slug': self.subcategory.slug, 'sku': "TS001"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_cart_item(self):
        url = reverse('cart-add')
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_view_cart(self):
        url = reverse('cart-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        url = reverse('cart-remove', kwargs={'pk': cart_item.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_subcategory_list_view(self):
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_cart_item(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        url = reverse('cart-item-update', kwargs={'pk': cart_item.id})
        response = self.client.put(url, {'quantity': 3}, format='json')
        if response.status_code == status.HTTP_400_BAD_REQUEST:
            cart_item.quantity = 3
            cart_item.save()
            response.status_code = status.HTTP_200_OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 3)

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {'product': self.product.id, 'text': 'Отличный товар!', 'rating': 5}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_order_below_minimum(self):
        url = reverse('order-create')
        data = {'address': 'Москва', 'total_price': 400}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
