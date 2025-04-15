import React from "react";
import ProductCard from "../components/ProductCard";
import 'bootstrap/dist/css/bootstrap.min.css';

function Home() {
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
  );
}

export default Home;