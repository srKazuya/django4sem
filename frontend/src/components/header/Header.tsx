import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './Header.module.scss';
import logo from '@assets/img/logo.svg';
import likeIcon from '@assets/img/like.svg';
import profileIcon from '@assets/img/profile.svg';
import busketIcon from '@assets/img/busket.svg';
import { Link } from 'react-router-dom';

interface Subcategory {
  id: number;
  name: string;
  absolute_url?: string;
}

interface Category {
  id: number;
  name: string;
  absolute_url?: string;
  subcategories: Subcategory[];
}

const Header = () => {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/api/categories/')
      .then(response => {
        console.log('API response:', response.data); // Для отладки
        setCategories(response.data);
      })
      .catch(error => {
        console.error('Ошибка при загрузке категорий:', error);
      });
  }, []);

  if (!categories.length) {
    return <div>Загрузка...</div>;
  }

  return (
    <header className={styles.mainCont}>
      <nav className={styles.nav}>
        <div className={styles.logoCont}>
          <Link
          to ={``}
          > <img src={logo} alt="Логотип" className={styles.logo} />
          </Link>
        </div>

        <ul className={styles.menu}>
          {categories.map(category => (
            <li key={category.id} className={styles.menuItem}>
              <Link
                to={
                  category.absolute_url
                    ? new URL(category.absolute_url).pathname.replace('/api', '')
                    : `/category/${category.id}`
                }
                className={styles.menuLink}
              >
                {category.name}
              </Link>
              {category.subcategories.length > 0 && (
                <ul className={styles.submenu}>
                  {category.subcategories.map(subcategory => (
                    <li key={subcategory.id} className={styles.submenuItem}>
                      <Link
                        to={
                          subcategory.absolute_url
                            ? new URL(subcategory.absolute_url).pathname.replace('/api', '')
                            : `/subcategory/${subcategory.id}`
                        }
                        className={styles.submenuLink}
                      >
                        {subcategory.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              )}
            </li>
          ))}
        </ul>

        <div className={styles.buttons}>
          <button className={styles.button}>
            <img src={likeIcon} alt="Избранное" />
            <span>Избранное</span>
          </button>
          <button className={styles.button}>
            <img src={profileIcon} alt="Войти" />
            <span>Войти</span>
          </button>
          <button className={styles.button}>
            <img src={busketIcon} alt="Корзина" />
            <span>Корзина</span>
          </button>
        </div>
      </nav>
    </header>
  );
};

export default Header;