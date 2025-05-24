import React from "react";

function ProductCard({ product }) {
  return (
    <div className="card p-3 mb-3">
      <img src={product.imageUrl} className="card-img-top" style={{ maxHeight: "200px", objectFit: "cover" }} />
      <div className="card-body">
        <h5 className="card-title">{product.productName}</h5>
        <p className="card-text">Price: ${product.price}</p>
        <p className="card-text">Rating: {product.rating}</p>
        <p className="card-text">{product.description}</p>
      </div>
    </div>
  );
}

export default ProductCard;
