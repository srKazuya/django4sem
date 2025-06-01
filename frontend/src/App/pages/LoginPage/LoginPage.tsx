import { useState } from 'react';
import { useNavigate } from 'react-router-dom'; 
import axios from 'axios';
import styles from './LoginPage.module.scss'; 

const LoginPage = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/users/login/', formData);
      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      setMessage('Успешный вход');
      navigate('/');
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    } catch (error) {
      setMessage('Ошибка авторизации');
    }
  };

  const handleRegisterRedirect = () => {
    navigate('/register');
  };

  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <h2>Вход</h2>
        <input
          type="text"
          name="username"
          placeholder="Имя пользователя"
          onChange={handleChange}
          className={styles.input}
        />
        <input
          type="password"
          name="password"
          placeholder="Пароль"
          onChange={handleChange}
          className={styles.input}
        />
        <button type="submit" className={styles.button}>
          Войти
        </button>
        {message && <p className={styles.message}>{message}</p>}
      </form>
      <button onClick={handleRegisterRedirect} className={styles.registerButton}>
        Зарегистрироваться
      </button>
    </div>
  );
};

export default LoginPage;