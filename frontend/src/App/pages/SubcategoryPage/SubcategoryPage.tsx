import  { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import styles from './SubcategoryPage.module.scss';

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
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        setLoading(true);
        axios
            .get(`http://127.0.0.1:8000/api/subcategory/${slug}/`)
            .then((response) => {
                setSubcategory(response.data);
                return axios.get(`http://127.0.0.1:8000/api/products/?subcategory_slug=${slug}`);
            })
            .then((response) => {
                setProducts(response.data);
                setLoading(false);
            })
            .catch((error) => {
                console.error('Ошибка при загрузке данных:', error);
                setError('Не удалось загрузить подкатегорию или продукты');
                setLoading(false);
            });
    }, [slug]);

    const filteredProducts = products.filter((product) =>
        product.name.toLowerCase().includes(searchQuery.toLowerCase())
    );

    if (loading) {
        return <div className={styles.container}>Загрузка...</div>;
    }

    if (error) {
        return <div className={styles.container}>{error}</div>;
    }

    if (!subcategory) {
        return <div className={styles.container}>Подкатегория не найдена</div>;
    }

    return (
        <div className={styles.container}>
            {/* Заголовок */}
            <div className={styles.header}>
                <h1>{subcategory.name}</h1>
                <h2>ИНТЕРЬЕР</h2>
                <h3>МЕБЕЛЬ</h3>
            </div>

            {/* Бегущая строка с продуктами */}
            <div className={styles.marquee}>
                <div className={styles.marqueeContent}>
                    {products.concat(products).map((product, index) => (
                        <div key={`${product.id}-${index}`} className={styles.marqueeItem}>
                            <img
                                src={product.image || `https://via.placeholder.com/300x200?text=Product+${index + 1}`}
                                alt={product.name}
                            />
                        </div>
                    ))}
                </div>
            </div>

            {/* Поиск */}
            <div className={styles.search}>
                <input
                    type="text"
                    placeholder="Поиск..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </div>

            {/* Продукты */}
            <section className={styles.products}>
                {filteredProducts.length === 0 ? (
                    <p>Нет продуктов в этой подкатегории</p>
                ) : (
                    filteredProducts.map((product) => (
                        <div key={product.id} className={styles.productCard}>
                            <Link
                                to={
                                    product.absolute_url
                                        ? new URL(product.absolute_url).pathname.replace('/api', '')
                                        : `/subcategory/${subcategory.slug}/${product.slug}/${product.sku}`
                                }
                                className={styles.cardLink}
                            >
                                <div className={styles.cardContent}>
                                    <img
                                        src={product.image || `https://via.placeholder.com/300x200?text=Product+${product.id}`}
                                        alt={product.name}
                                    />
                                    <div className={styles.cardOverlay}>
                                        <h4>{product.name}</h4>
                                        <p>{product.price} ₽</p>
                                    </div>
                                </div>
                            </Link>
                        </div>
                    ))
                )}
            </section>
        </div>
    );
};

export default SubcategoryPage;