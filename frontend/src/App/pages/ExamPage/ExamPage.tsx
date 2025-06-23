import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface User {
    id: number;
    email: string;
}

interface Exam {
    id: number;
    title: string;
    created_at: string;
    exam_date: string;
    image: string | null;
    users: User[];
    is_public: boolean;
}

interface ApiResponse {
    title: string;
    exams: Exam[];
}

const ExamPage = () => {
    const [data, setData] = useState<ApiResponse | null>(null);
    const [error, setError] = useState<string>('');

    useEffect(() => {
        axios.get<ApiResponse>('http://127.0.0.1:8000/api/exam/')
            .then(res => setData(res.data))
            .catch(() => setError('Ошибка загрузки данных'));
    }, []);

    if (error) return <div>{error}</div>;
    if (!data) return <div>Загрузка...</div>;

    return (
        <div>
            <h1>{data.title}</h1>
            {data.exams.length === 0 ? (
                <p>Нет опубликованных экзаменов</p>
            ) : (
                data.exams.map(exam => (
                    <div key={exam.id} style={{ border: '1px solid #000', marginBottom: 10, padding: 10 }}>
                        <h2>Название экзамена: {exam.title}</h2>
                        <p><strong>Дата создания записи:</strong> {new Date(exam.created_at).toLocaleString()}</p>
                        <p><strong>Дата проведения экзамена:</strong> {exam.exam_date}</p>
                        <p><strong>Изображение:</strong></p>
                        {exam.image ? (
                            <img src={exam.image} alt="Задание по экзамену" style={{ maxWidth: 200 }} />
                        ) : (
                            <p>Изображение отсутствует</p>
                        )}
                        <p><strong>Пользователи, которые пишут экзамен:</strong></p>
                        <ul>
                            {exam.users.map(user => (
                                <li key={user.id}>{user.email}</li>
                            ))}
                        </ul>
                        <p><strong>Опубликовано:</strong> {exam.is_public ? 'Да' : 'Нет'}</p>
                    </div>
                ))
            )}
        </div>
    );
};

export default ExamPage;
