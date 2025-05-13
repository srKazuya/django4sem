import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

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
  const { productSlug, sku } = useParams<{ slug: string; productSlug: string; sku: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    axios
      .get(`http://127.0.0.1:8000/api/products/${productSlug}/${sku}/`)
      .then(response => {
        setProduct(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка при загрузке продукта:', error);
        setError('Не удалось загрузить продукт');
        setLoading(false);
      });
  }, [productSlug, sku]);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!product) {
    return <div>Продукт не найден</div>;
  }

  return (
    <div>
      <h1>{product.name}</h1>
      {product.image && (
        <img src={product.image} alt={product.name} style={{ maxWidth: '300px' }} />
      )}
      <p>Артикул: {product.sku}</p>
      <p>Цена: {product.price} руб.</p>
      <p>В наличии: {product.stock} шт.</p>
      <p>Подкатегория: {product.subcategory.name}</p>
      <p>Описание: {product.description}</p>
    </div>
  );
};

export default ProductPage;