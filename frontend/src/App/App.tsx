
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import Main from '@pages/Main'
import CategoryPage from '@pages/CategoryPage';
import SubcategoryPage from '@pages/SubcategoryPage';
import ProductPage from '@pages/ProductPage';
import Header from '@components/header'
import styles from './App.module.scss';

const App = () => {

  return (
    <div className={styles.cont}>
      <Router>
        <Header />
        <Routes>
          <Route path="*" element={<Main />} />
          <Route path="/category/:slug" element={<CategoryPage />} />
          <Route path="/subcategory/:slug" element={<SubcategoryPage />} />
          <Route path="/subcategory/:slug/:productSlug/:sku" element={<ProductPage />} />

        </Routes>
      </Router>
    </div>
  );
};

export default App