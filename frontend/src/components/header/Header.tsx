
import styles from './Header.module.scss'

const Header = () => {
    return (
    <div className={`${styles.mainCont}`}>
        HEADER
    </div>
    )
};

export default Header;


// import React from 'react';
// import { useLocation } from 'react-router-dom';

// const Header = () => {
//   const location = useLocation();
  
//   return (
//     <header>
//       {location.pathname === '/special-page' ? (
//         <SpecialHeader /> // Ваш особый хедер
//       ) : (
//         <DefaultHeader /> // Стандартный хедер
//       )}
//     </header>
//   );
// };

// export default Header;