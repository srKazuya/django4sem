import bgImg from '@assets/img/bgImg.jpg';
import styles from './Main.module.scss';


const Main = () => {
    return <div className={styles.backCont}>
        <img className={styles.backImg} src={bgImg} alt="" />
    </div>;
};

export default Main;