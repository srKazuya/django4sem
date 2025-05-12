import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Header.module.scss';
import logo from '@assets/img/logo.svg'

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
    axios.get('http://127.0.0.1:8000/api/categories/')
      .then(response => {
        setCategories(response.data);
      })
      .catch(error => {
        console.error('Ошибка при загрузке категорий:', error);
      });
  }, []);


  const middleIndex = Math.ceil(categories.length / 2);
  const firstHalf = categories.slice(0, middleIndex);
  const secondHalf = categories.slice(middleIndex);

  return (
    <header className={`${styles.mainCont}`}>
      <nav className={styles.nav}>
        <ul className={styles.leftMenu}>
          {firstHalf.map(category => (
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

        <div className={styles.logoCont}>
          <img src={logo} alt="Логотип" className={styles.logo} />
        </div>

        <ul className={styles.rightMenu}>
          {secondHalf.map(category => (
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