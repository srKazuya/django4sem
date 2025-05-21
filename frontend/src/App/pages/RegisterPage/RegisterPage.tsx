import axios from 'axios';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './RegisterPage.module.scss';

const RegisterPage = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '' });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    setError('');
    try {
      await axios.post('http://127.0.0.1:8000/api/users/register/', formData);
      setMessage('Регистрация успешна!');
      setTimeout(() => navigate('/login'), 1000); 
    } catch (err: any) {
      if (err.response && err.response.data) {
        const errorMessages = Object.values(err.response.data).flat().join(' ');
        setError(`Ошибка регистрации: ${errorMessages}`);
      } else {

        setError('Ошибка регистрации. Попробуйте снова.');
      }
    }
  };

  return (
    <div className={styles.container}>
      <form onSubmit={handleSubmit} className={styles.form}>
        <h2>Регистрация</h2>
        <input
          type="text"
          name="username"
          placeholder="Имя пользователя"
          onChange={handleChange}
          className={styles.input}
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
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
          Зарегистрироваться
        </button>
        {message && <p className={styles.success}>{message}</p>}
        {error && <p className={styles.error}>{error}</p>}
      </form>
    </div>
  );
};

export default RegisterPage;