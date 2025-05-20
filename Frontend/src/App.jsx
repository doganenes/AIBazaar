import "./App.css";
import Home from "../pages/Home";
import Signin from "../pages/Signin";
import Signup from "../pages/Signup";
import NotFound from "../pages/NotFound";
import { Container } from "react-bootstrap";
import Header from "../components/Header";
import { Route, Routes } from "react-router-dom";
import GeneratePrice from "../pages/GeneratePrice";
import Favorites from "../pages/Favorites";
import ProductDetail from "../pages/ProductDetail";
import "bootstrap/dist/css/bootstrap.min.css";
import '@fortawesome/fontawesome-free/css/all.min.css';
import Footer from "../components/Footer";
function App() {
  return (
    <div>
      <Container>
        <Header />
        <Routes>
          <Route path="/" element={<Signin />}></Route>
          <Route path="/home" element={<Home />}></Route>
          <Route path="/signup" element={<Signup />}></Route>
          <Route path="/signin" element={<Signin />}></Route>
          <Route path="/generate-price" element={<GeneratePrice />}></Route>
          <Route path="/favorites" element={<Favorites />}></Route>
          <Route path="/product-detail" element={<ProductDetail />}></Route>
          <Route path="*" element={<NotFound />}></Route>
        </Routes>
      </Container>
        <Footer />
    </div>
  );
}

export default App;
