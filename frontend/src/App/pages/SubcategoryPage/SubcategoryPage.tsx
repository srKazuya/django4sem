import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';

interface Subcategory {
    id: number;
    name: string;
    slug: string;
    absolute_url?: string;
}

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
    subcategory: Subcategory;
}

const SubcategoryPage = () => {
    const { slug } = useParams<{ slug: string }>();
    const [subcategory, setSubcategory] = useState<Subcategory | null>(null);
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        axios
            .get(`http://127.0.0.1:8000/api/subcategory/${slug}/`)
            .then(response => {
                setSubcategory(response.data);
                return axios.get(`http://127.0.0.1:8000/api/products/?subcategory_slug=${slug}`);
            })
            .then(response => {
                setProducts(response.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных:', error);
                setError('Не удалось загрузить подкатегорию или продукты');
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
            <h2>Продукты</h2>
            {products.length === 0 ? (
                <p>Нет продуктов в этой подкатегории</p>
            ) : (
                <ul>
                    {products.map(product => (
                        <li key={product.id}>
                            <Link
                                to={
                                    product.absolute_url
                                        ? new URL(product.absolute_url).pathname.replace('/api', '')
                                        : `/subcategory/${subcategory.slug}/${product.slug}/${product.sku}`
                                }
                            >
                                <h3>{product.name}</h3>
                            </Link>
                            {product.image && (
                                <img src={product.image} alt={product.name} style={{ maxWidth: '200px' }} />
                            )}
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