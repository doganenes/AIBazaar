import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "../css/ProductCard.css";

function ProductCard({ product }) {
  return (
    <div className="card h-100 border-0 shadow-sm product-card">
      <div className="position-relative overflow-hidden">
        <img
          src={"https://placehold.co/600x400"}
          className="card-img-top"
          style={{ height: "250px", objectFit: "cover" }}
          alt={product.productName}
        />

        <div className="card-overlay position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center">
          <button className="btn btn-light btn-sm me-2 overlay-btn">
            <i className="fas fa-eye"></i> Display
          </button>
          <button className="btn btn-danger btn-sm overlay-btn">
            <i className="fas fa-heart"></i>
          </button>
        </div>

        <div className="position-absolute top-0 end-0 m-3">
          <span className="badge bg-primary fs-6 px-3 py-2">
            ${product.price}
          </span>
        </div>
      </div>

      <div className="card-body d-flex flex-column">
        <h5
          className="card-title fw-bold text-truncate"
          title={product.productName}
        >
          {product.productName}
        </h5>

        <p
          className="card-text text-muted small flex-grow-1"
          style={{
            display: "-webkit-box",
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
          }}
        >
          {product.description}
        </p>
      </div>
    </div>
  );
}

export default ProductCard;