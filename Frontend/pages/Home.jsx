import { Form, Button } from "react-bootstrap";
import { login, tokenToId } from "../api/api";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import { getAllProducts } from "../api/api";

const Home = () => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (!token) {
      navigate("/signin");
    } else {
      getAllProducts()
        .then((data) => setProducts(data))
        .catch((err) => console.error("Error loading products:", err));
    }
  }, [navigate]);

  return (
    <div className="container-fluid">
      <div className="row">
        {products.map((product) => (
          <div className="col-md-3 mt-5" key={product.productID}>
            <ProductCard product={product} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
