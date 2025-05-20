import { Form, Button } from "react-bootstrap";
import "../css/Signin.css";
import { login, tokenToId } from "../api/api";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProductCard from "../components/ProductCard";

const Home = () => {
const navigate = useNavigate();
useEffect(() => {
  const token = localStorage.getItem("authToken");
  if (!token) {
    navigate("/signin");
  }
}, [navigate]);
  return (
      <div>
      <div className="container-fluid">
        <div className="row">
          <div className="col">
            <ProductCard />
          </div>
          <div className="col">
            <ProductCard />
          </div>
          <div className="col">
            <ProductCard />
          </div>
          <div className="col">
            <ProductCard />
          </div>
        </div>
        <div className="row my-3">
          <div className="col">
            <ProductCard />
          </div>
          <div className="col">
            <ProductCard />
          </div>
          <div className="col">
            <ProductCard />
          </div>
          <div className="col">
            <ProductCard />
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home