import { Key, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import styles from './Header.module.scss';
import logo from '@assets/img/logo.svg';
import likeIcon from '@assets/img/like.svg';
import profileIcon from '@assets/img/profile.svg';
import burger from '@assets/img/burger.svg'
import busketIcon from '@assets/img/busket.svg';
import { Link } from 'react-router-dom';

const Header = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('access')); // Проверяем токен при загрузке
  const [isMenuOpen, setIsMenuOpen] = useState(false); // Состояние для бургер-меню
  const navigate = useNavigate();


  useEffect(() => {

    axios
      .get('http://127.0.0.1:8000/api/categories/')
      .then(response => {
        setCategories(response.data);
      })
      .catch(error => {
        console.error('Ошибка при загрузке категорий:', error);
      });
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      const tokenExists = !!localStorage.getItem('access');
      setIsAuthenticated(tokenExists);
    }, 500);

    return () => clearInterval(interval);
  }, []);

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleLogoutClick = () => {
    localStorage.removeItem('access');
    setIsAuthenticated(false);
    navigate('/');
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  if (!categories.length) {
    return <div>Загрузка...</div>;
  }

  return (
    <header className={styles.mainCont}>
      <nav className={styles.nav}>
        <div className={styles.logoCont}>
          <Link to="">
            <img src={logo} alt="Логотип" className={styles.logo} />
          </Link>
        </div>

        <button className={styles.burgerButton} onClick={toggleMenu}>
          <img src={burger} alt="Меню" />
        </button>

        <ul className={`${styles.menu} ${isMenuOpen ? styles.menuOpen : ''}`}>
          {categories.map(category => (
            <li key={category.id} className={styles.menuItem}>
              <Link
                to={
                  category.absolute_url
                    ? new URL(category.absolute_url).pathname.replace('/api/categories', 'category')
                    : `/category/${category.id}`
                }
                className={styles.menuLink}
              >
                {category.name}
              </Link>
              {category.subcategories.length > 0 && (
                <ul className={styles.submenu}>
                  {category.subcategories.map((subcategory: { id: Key | null | undefined; absolute_url: string | URL; name: unknown; }) => (
                    <li key={subcategory.id} className={styles.submenuItem}>
                      <Link
                        to={
                          subcategory.absolute_url
                            ? new URL(subcategory.absolute_url).pathname.replace('/api/subcategories', 'subcategory')
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

        <div className={styles.buttonsDesktop}>
          <button className={styles.button}>
            <img src={profileIcon} alt="Избранное" />
            <span>Профиль</span>
          </button>
          {isAuthenticated ? (
            <button className={styles.button} onClick={handleLogoutClick}>
              <img src={profileIcon} alt="Выйти" />
              <span>Выйти</span>
            </button>
          ) : (
            <button className={styles.button} onClick={handleLoginClick}>
              <img src={profileIcon} alt="Войти" />
              <span>Войти</span>

            </button>
          )}

          <button className={styles.button}>
            <Link to="/cart">
              <img src={busketIcon} alt="Корзина" />
              <span>Корзина</span>
            </Link>

          </button>


        </div>
      </nav>

      <div className={styles.buttonsMobile}> {/* Добавлен контейнер для мобильной версии */}
        <button className={styles.button}>
          <img src={profileIcon} alt="Избранное" />
          <span>Профиль</span>
        </button>
        {isAuthenticated ? (
          <button className={styles.button} onClick={handleLogoutClick}>
            <img src={profileIcon} alt="Выйти" />
            <span>Выйти</span>
          </button>
        ) : (
          <button className={styles.button} onClick={handleLoginClick}>
            <img src={profileIcon} alt="Войти" />
            <span>Войти</span>
          </button>
        )}
        <button className={styles.button}>
          <img src={busketIcon} alt="Корзина" />
          <span>Корзина</span>
        </button>
      </div>
    </header>
  );
};

export default Header;