import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

interface Category {
  id: number;
  name: string;
  slug: string;
  absolute_url?: string;
  subcategories: Subcategory[];
}

interface Subcategory {
  id: number;
  name: string;
  slug: string;
  absolute_url?: string;
}

const CategoryPage = () => {
  const { slug } = useParams<{ slug: string }>();
  const [category, setCategory] = useState<Category | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    axios
      .get(`http://127.0.0.1:8000/api/category/${slug}/`)
      .then(response => {
        setCategory(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Ошибка при загрузке категории:', error);
        setError('Не удалось загрузить категорию');
        setLoading(false);
      });
  }, [slug]);

  if (loading) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!category) {
    return <div>Категория не найдена</div>;
  }

  return (
    <div>
      <h1>{category.name}</h1>
      <h2>Подкатегории</h2>
      {category.subcategories.length === 0 ? (
        <p>Нет подкатегорий</p>
      ) : (
        <ul>
          {category.subcategories.map(subcategory => (
            <li key={subcategory.id}>
              <Link
                to={
                  subcategory.absolute_url
                    ? new URL(subcategory.absolute_url).pathname.replace('/api', '')
                    : `/subcategory/${subcategory.slug}`
                }
              >
                {subcategory.name}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default CategoryPage;