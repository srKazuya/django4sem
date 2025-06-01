import { useEffect, useState } from 'react';
import axios from 'axios';
import styles from './PromotionWidget.module.scss';

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
    sku: string;
}

const PromotionWidget = () => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        axios.get('http://127.0.0.1:8000/api/promotions/')
            .then(response => {
                setProducts(response.data.map((promotion: { id: number; image: string | null }) => ({
                    id: promotion.id,
                    image: promotion.image || `https://via.placeholder.com/300x200?text=Promotion+${promotion.id}`
                })));
                setLoading(false);
            })
            .catch(() => {
                setError('Failed to load promotions');
                setLoading(false);
            });
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className={styles.widgetContainer}>
            <h3>Акции</h3>
            <div className={styles.productsList}>
                {products.map(product => (
                    <div key={product.id} className={styles.productCard}>
                        <img
                            src={product.image}
                            alt={`Promotion ${product.id}`}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PromotionWidget;