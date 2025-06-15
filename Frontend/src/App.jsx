import "./App.css";
import "@fortawesome/fontawesome-free/css/all.min.css";
import Home from "../src/pages/Home";
import Signin from "../src/pages/Signin";
import Signup from "../src/pages/Signup";
import NotFound from "../src/pages/NotFound";
import { Container } from "react-bootstrap";
import Header from "../src/components/Header";
import { Route, Routes, useLocation } from "react-router-dom";
import GeneratePrice from "../src/pages/GeneratePrice";
import Favorites from "../src/pages/Favorites";
import ProductDetail from "../src/pages/ProductDetail";
import "bootstrap/dist/css/bootstrap.min.css";
import Footer from "../src/components/Footer";
import { useState } from "react";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  const location = useLocation();
  const [searchTerm, setSearchTerm] = useState("");
  const authPages = ["/", "/signin", "/signup"];
  const shouldShowHeader = !authPages.includes(location.pathname);

  return (
    <div className="d-flex flex-column min-vh-100">
      {shouldShowHeader && <Header setSearchTerm={setSearchTerm} />}

      <Container className="flex-grow-1">
        <Routes>
          <Route path="/" element={<Signin />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/signin" element={<Signin />} />
          <Route element={<PrivateRoute />}>
            <Route path="/home" element={<Home searchTerm={searchTerm} />} />
            <Route path="/generatePrice" element={<GeneratePrice />} />
            <Route path="/favorites" element={<Favorites />} />
            <Route path="/productDetail/:id" element={<ProductDetail />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Container>

      {shouldShowHeader && <Footer />}
    </div>
  );
}

export default App;
