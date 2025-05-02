
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import Main from '@pages/Main'
import Header from '@components/header'
const App = () => {

  return (
    <div className='cont'>
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