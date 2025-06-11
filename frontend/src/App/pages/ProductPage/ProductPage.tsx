import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // Убедитесь, что библиотека установлена: npm install jwt-decode

type Comment = {
  id: number;
  user: string;
  userId: number; // Добавлено поле для идентификатора пользователя
  text: string;
  rating: number;
};

interface Product {
  id: number;
  name: string;
  slug: string;
  sku: string;
  price: string;
  stock: number;
  image: string;
  description: string;
  absolute_url?: string;
  subcategory: {
    id: number;
    name: string;
    slug: string;
    absolute_url?: string;
  };
}

const ProductPage = () => {
  const { productSlug, sku } = useParams();
  const [product, setProduct] = useState<Product | null>(null);
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');
  const [rating, setRating] = useState(3);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingCommentId, setEditingCommentId] = useState<number | null>(null);
  const [editingText, setEditingText] = useState('');
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);

  useEffect(() => {
    // Получение текущего пользователя из токена
    const token = localStorage.getItem('access');
    if (token) {
      const decodedToken: any = jwtDecode(token);
      setCurrentUserId(decodedToken.user_id);
    }

    setLoading(true);
    axios
      .get(`http://127.0.0.1:8000/api/products/${productSlug}/${sku}/`)
      .then((response) => {
        setProduct(response.data);
        return axios.get(`http://127.0.0.1:8000/api/comments/?product=${response.data.id}`);
      })
      .then((response) => {
        setComments(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Ошибка при загрузке данных:', error);
        setError('Не удалось загрузить данные');
        setLoading(false);
      });
  }, [productSlug, sku]);

  const handleAddComment = () => {
    if (!product) {
      console.error('Продукт не загружен');
      return;
    }
    const token = localStorage.getItem('access');
    if (!token) {
      console.error('Токен авторизации отсутствует');
      return;
    }
    axios
      .post(
        'http://127.0.0.1:8000/api/comments/',
        { product: product.id, text: newComment, rating },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((response) => {
        setComments([...comments, response.data]);
        setNewComment('');
        setRating(3);
      })
      .catch((error) => {
        console.error('Ошибка при добавлении комментария:', error);
      });
  };

  const handleDeleteComment = (id: number) => {
    const token = localStorage.getItem('access');
    if (!token) {
      console.error('Токен авторизации отсутствует');
      return;
    }
    axios
      .delete(`http://127.0.0.1:8000/api/comments/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => {
        setComments(comments.filter((comment) => comment.id !== id));
      })
      .catch((error) => {
        console.error('Ошибка при удалении комментария:', error);
      });
  };

  const handleEditComment = (id: number) => {
    const token = localStorage.getItem('access');
    if (!token) {
      console.error('Токен авторизации отсутствует');
      return;
    }
    axios
      .patch(
        `http://127.0.0.1:8000/api/comments/${id}/`,
        { text: editingText },
        { headers: { Authorization: `Bearer ${token}` } }
      )
      .then((response) => {
        setComments(
          comments.map((comment) =>
            comment.id === id ? { ...comment, text: response.data.text } : comment
          )
        );
        setEditingCommentId(null);
        setEditingText('');
      })
      .catch((error) => {
        console.error('Ошибка при редактировании комментария:', error);
      });
  };

    const addToCart = async (productId: number, quantity: number = 1) => {
      const token = localStorage.getItem('access');
      try {
        await axios.post(
          'http://127.0.0.1:8000/api/cart/add/',
          {
            product_id: productId,
            quantity,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        
        console.log('Item added to cart successfully');
      } catch (err: any) {
        if (err.response?.status === 400) {
          alert(err.response.data?.quantity || 'Товара нет на складе');
        } else {
          console.error(err);
        }
      }
    };
  
    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>{error}</div>;
  
    return (
      <div>
        <h1>{product!.name}</h1>
        {product!.image && (
          <img src={product!.image} alt={product!.name} style={{ maxWidth: '300px' }} />
        )}
        <p>Артикул: {product!.sku}</p>
        <p>Цена: {product!.price} руб.</p>
        <p>В наличии: {product!.stock} шт.</p>
        <p>Подкатегория: {product!.subcategory.name}</p>
        <p>Описание: {product!.description}</p>
        <button onClick={() => addToCart(product!.id)}>Добавить в корзину</button>
  
        <h2>Комментарии</h2>
        {comments.length > 0 ? (
          comments.map((comment) => (
            <div key={comment.id}>
              {editingCommentId === comment.id ? (
                <div>
                  <textarea
                    value={editingText}
                    onChange={(e) => setEditingText(e.target.value)}
                  />
                  <button onClick={() => handleEditComment(comment.id)}>Сохранить</button>
                  <button onClick={() => setEditingCommentId(null)}>Отмена</button>
                </div>
              ) : (
                <p>
                  <strong>{comment.user}</strong>: {comment.text} ({comment.rating}/5)
                </p>
              )}
              {comment.userId === currentUserId && (
                <div>
                  <button onClick={() => setEditingCommentId(comment.id)}>Редактировать</button>
                  <button onClick={() => handleDeleteComment(comment.id)}>Удалить</button>
                </div>
              )}
            </div>
          ))
        ) : (
          <p>Комментариев пока нет.</p>
        )}
  
        <h3>Добавить комментарий</h3>
        <textarea
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Ваш комментарий"
        />
        <select value={rating} onChange={(e) => setRating(Number(e.target.value))}>
          {[1, 2, 3, 4, 5].map((r) => (
            <option key={r} value={r}>
              {r}
            </option>
          ))}
        </select>
        <button onClick={handleAddComment} disabled={!product}>Добавить</button>
      </div>
    );
  };
  
  export default ProductPage;