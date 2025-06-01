// import bgImg from '@assets/img/bgImg.jpg';
import styles from './Main.module.scss';
import PopularProductsWidget from './components/PopularProductsWidget';
import PromotionWidget from './components/PromotionWidget';
import NewProductsWidget from './components/NewProductsWidget';
// import bgImg from '@assets/img/scandica_matias_1.jpg'



const Main = () => {
    return <div className={styles.main_cont}>
        {/* <figure>
        <figcaption>
        Кухня в стиле "Retro"
        </figcaption>
        <img className={styles.mainImg} src={bgImg} alt="" />
        </figure> */}
        <PopularProductsWidget />
        <NewProductsWidget />
        <PromotionWidget /> 
    </div>;

};

export default Main;