// import bgImg from '@assets/img/bgImg.jpg';
// import styles from './Main.module.scss';
import PopularProductsWidget from './components/PopularProductsWidget';
import PromotionWidget from './components/PromotionWidget';
import NewProductsWidget from './components/NewProductsWidget';




const Main = () => {
    return <div>
        {/* <img className={styles.backImg} src={bgImg} alt="" /> */}
        <PromotionWidget />
        <PopularProductsWidget />
        <NewProductsWidget />
    </div>;
};

export default Main;