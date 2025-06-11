import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import styles from './CartPage.module.scss';

interface Product {
  name: string;
  price: number;
}

interface CartItem {
  id: number;
  product: Product;
  quantity: number;
}

interface Cart {
  items: CartItem[];
}

interface DecodedToken {
  exp: number;
  user_id: number;
}

const CartPage = () => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('access');

    if (!token) {
      setError('Not authenticated');
      setLoading(false);
      return;
    }

    try {
      const decoded: DecodedToken = jwtDecode(token);
      const currentTime = Math.floor(Date.now() / 1000);
      if (decoded.exp < currentTime) {
        setError('Token expired');
        setLoading(false);
        return;
      }
    } catch (err) {
      setError('Invalid token');
      setLoading(false);
      return;
    }

    const fetchCart = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/cart/view/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        console.log('Cart data:', response.data);
        setCart(response.data);
      } catch (err) {
        console.error('Cart load error:', err);
        setError('Failed to load cart data.');
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div className={styles.backCont}>
      <h1>Ваша корзина</h1>
      {cart && cart.items && cart.items.length > 0 ? (
        <div>
          {cart.items.map((item) => (
            <div key={item.id} className={styles.cartItem}>
              <span>{item.product.name}</span>
              <span>Количество: {item.quantity}</span>
              <span>Цена: {item.product.price}₽ </span>
            </div>
          ))}
        </div>
      ) : (
        <div>Корзина пуста.</div>
      )}
    </div>
  );
};

export default CartPage;
