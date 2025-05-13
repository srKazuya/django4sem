import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

interface Subcategory {
    id: number;
    name: string;
    absolute_url?: string;
}

interface Product {
    id: number;
    name: string;
    image: string;
    sku: string;
    price: string;
    stock: number;
    description: string;
    subcategory: Subcategory;
}

const SubcategoryPage = () => {
    const { slug } = useParams<{ slug: string }>();
    const [subcategory, setSubcategory] = useState<Subcategory | null>(null);
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Загружаем подкатегорию
        setLoading(true);
        axios
            .get(`http://127.0.0.1:8000/api/subcategory/${slug}/`)
            .then(response => {
                setSubcategory(response.data);
                // Загружаем продукты после получения подкатегории
                return axios.get('http://127.0.0.1:8000/api/products/');
            })
            .then(response => {
                // Фильтруем продукты по subcategory.id
                const filteredProducts = response.data.filter(
                    (product: Product) => product.subcategory.id === subcategory?.id
                );
                setProducts(filteredProducts);
                setLoading(false);
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
                setError('Не удалось загрузить данные');
                setLoading(false);
            });
    }, [slug]);

    if (loading) {
        return <div>Загрузка...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!subcategory) {
        return <div>Подкатегория не найдена</div>;
    }

    return (
        <div>
            <h1>{subcategory.name}</h1>
            <p>ID: {subcategory.id}</p>
            <p>URL: {subcategory.absolute_url}</p>
            <h2>Продукты</h2>
            {products.length === 0 ? (
                <p>Нет продуктов в этой подкатегории</p>
            ) : (
                <ul>
                    {products.map(product => (
                        <li key={product.id}>
                            <h3>{product.name}</h3>
                            <img src={product.image} alt={product.name} style={{ maxWidth: '200px' }} />
                            <p>Артикул: {product.sku}</p>
                            <p>Цена: {product.price} руб.</p>
                            <p>В наличии: {product.stock} шт.</p>
                            <p>{product.description}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default SubcategoryPage;