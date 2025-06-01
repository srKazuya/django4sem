import { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import styles from './PopularProductsWidget.module.scss';

interface Product {
    id: number;
    name: string;
    price: string;
    image: string;
    absolute_url?: string;
    subcategory?: {
        slug: string;
    };
    slug?: string;
    sku:string;
}

const PopularProductsWidget = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/products/high_rating/')
            .then(response => {
                setProducts(response.data);
                setLoading(false);
            })
            .catch(() => {
                setError('Failed to load popular products');
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className={styles.widgetContainer}>
            <h3>Популярные продукты</h3>
            <div className={styles.productsList}>
                {products.map(product => (
                    <div key={product.id} className={styles.productCard}>
                        <Link
                            to={`/subcategory/${product.subcategory?.slug}/${product.slug}/${product.sku}`}
                            className={styles.productLink}
                        >
                            <img
                                src={product.image || `https://via.placeholder.com/300x200?text=Product+${product.id}`}
                                alt={product.name}
                            />
                            <div>
                                <h4>{product.name}</h4>
                                <p>{product.price} ₽</p>
                            </div>
                        </Link>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PopularProductsWidget;