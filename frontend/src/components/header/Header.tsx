import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Header.module.scss';

interface Subcategory {
  id: number;
  name: string;
}

interface Category {
  id: number;
  name: string;
  subcategories: Subcategory[];
}

const Header = () => {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    // Запрос данных для хедера
    axios.get('http://127.0.0.1:8000/api/categories/')
      .then(response => {
        setCategories(response.data); // Устанавливаем данные в состояние
      })
      .catch(error => {
        console.error('Ошибка при загрузке категорий:', error);
      });
  }, []);

  return (
    <header className={`${styles.mainCont}`}>
      <nav>
        <ul className={styles.menu}>
          {categories.map(category => (
            <li key={category.id} className={styles.menuItem}>
              {category.name}
              {category.subcategories.length > 0 && (
                <ul className={styles.submenu}>
                  {category.subcategories.map(subcategory => (
                    <li key={subcategory.id} className={styles.submenuItem}>
                      {subcategory.name}
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>
      </nav>
    </header>
  );
};

export default Header;