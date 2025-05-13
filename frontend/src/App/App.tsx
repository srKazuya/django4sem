
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import Main from '@pages/Main'
// import CategoryPage from '@pages/CategoryPage';
import SubcategoryPage from '@pages/SubcategoryPage';
import Header from '@components/header'
import styles from './App.module.scss';

const App = () => {

  return (
    <div className={styles.cont}>
      <Router>
        <Header />
        <Routes>
          <Route path="*" element={<Main />} />
          {/* <Route path="/category/:id" element={<CategoryPage />} /> */}
          <Route path="/subcategory/:slug" element={<SubcategoryPage />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App