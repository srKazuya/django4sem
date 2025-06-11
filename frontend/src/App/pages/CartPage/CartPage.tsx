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

const CreateOrderForm = () => {
  const [address, setAddress] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleOrderSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const token = localStorage.getItem('access');
    if (!token) {
      setError('Not authenticated');
      setLoading(false);
      return;
    }

    try {
      await axios.post(
        'http://127.0.0.1:8000/api/order/create/',
        { address },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setSuccess(true);
      setAddress('');
    } catch {
      setError('Failed to create order.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Создать заказ</h2>
      {success && <p>Заказ успешно создан!</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <form onSubmit={handleOrderSubmit}>
        <label>
          Адрес:
          <input
            type="text"
            value={address}
            onChange={(e) => setAddress(e.target.value)}
            required
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Оформление заказа...' : 'Оформить заказ'}
        </button>
      </form>
    </div>
  );
};

const CartPage = () => {
  const [cart, setCart] = useState<Cart | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const updateQuantity = async (itemId: number, quantity: number) => {
    const token = localStorage.getItem('access');
    if (!token) return;

    try {
      await axios.patch(
        `http://127.0.0.1:8000/api/cart/item/${itemId}/`,
        { quantity },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      // Обновляем корзину локально
      setCart((prevCart) => {
        if (!prevCart) return prevCart;
        const updatedItems = prevCart.items.map((item) =>
          item.id === itemId ? { ...item, quantity } : item
        );
        return { ...prevCart, items: updatedItems };
      });
    } catch {
      console.error('Ошибка обновления количества');
    }
  };

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
              <span>Цена: {item.product.price}₽</span>
              <div>
                <button onClick={() => updateQuantity(item.id, item.quantity - 1)} disabled={item.quantity <= 1}>−</button>
                <span>{item.quantity}</span>
                <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>+</button>
              </div>
            </div>

          ))}
          <p className={styles.total}>
            <strong>Итого:</strong>{' '}
            {cart.items.reduce((sum, item) => sum + item.product.price * item.quantity, 0)} ₽
          </p>
        </div>
      ) : (
        <div>Корзина пуста.</div>
      )}
      <CreateOrderForm />
    </div>
  );
};

export default CartPage;
