import "./App.css";
import Home from "../pages/Home";
import Signin from "../pages/Signin";
import Signup from "../pages/Signup";
import NotFound from "../pages/NotFound";
import "@fortawesome/fontawesome-free/css/all.min.css";
import { Container } from "react-bootstrap";
import Header from "../components/Header";
import { Route, Routes } from "react-router-dom";
import GeneratePrice from "../pages/GeneratePrice";
import Favorites from "../pages/Favorites";
import ProductDetail from "../pages/ProductDetail";
import "bootstrap/dist/css/bootstrap.min.css";
import Footer from "../components/Footer";

function App() {
  return (
    <div className="d-flex flex-column min-vh-100">
      <Header />

      <Container className="flex-grow-1">
        <Routes>
          <Route path="/" element={<Signin />} />
          <Route path="/home" element={<Home />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/signin" element={<Signin />} />
          <Route path="/generatePrice" element={<GeneratePrice />} />
          <Route path="/favorites" element={<Favorites />} />
          <Route path="/productDetail" element={<ProductDetail />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Container>

      <Footer />
    </div>
  );
}

export default App;
