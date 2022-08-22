import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import History from "./pages/History";
import HistoryList from "./pages/HistoryList";
import HistoryDetail from "./pages/HistoryDetail";
import About from "./pages/About";

import Navbar from "./components/Navbar";

const App = () => {
  return (
    <React.StrictMode>
      <Router>
        <Navbar />
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/riwayat' element={<History />}>
            <Route path='' element={<HistoryList />} />
            <Route path=':postSlug' element={<HistoryDetail />} />
          </Route>
          <Route path='/tentang' element={<About />} />
        </Routes>
      </Router>
    </React.StrictMode>
  );
};

export default App;
