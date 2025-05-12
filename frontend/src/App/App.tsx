
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import Main from '@pages/Main'
import Header from '@components/header'
import styles from './App.module.scss';

const App = () => {

  return (
    <div className={styles.cont}>
      <Router>
        <Header />
        <Routes>
          <Route path="*" element={<Main />} />
        </Routes>
      </Router>
    </div>
  );
};

export default App