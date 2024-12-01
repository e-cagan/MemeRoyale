import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Form from './components/Form';
import Home from './components/Home';
import Navbar from './components/Navbar'; // Navbar'ı dahil et

function App() {
  return (
    <Router>
      <Navbar />  {/* Navbar'ı üstte yerleştir */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Form method="login" />} />
        <Route path="/register" element={<Form method="register" />} />
      </Routes>
    </Router>
  );
}

export default App;
