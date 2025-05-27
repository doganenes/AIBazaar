import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import { getAllProducts } from "../api/api";
import "../css/Home.css";

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
    <div className="container-fluid homeContainer">
      <div className="row mt-5">
        {products.map((product) => (
          <div className="col-md-3 mt-3" key={product.productID}>
            <ProductCard product={product} />
          </div>
        ))}
      </div>
    </div>
  );
  
};

export default Home;