import React from "react";
import "../css/ProductCard.css";
import { Link } from "react-router-dom";
import { addFavoriteProduct } from "../api/api";
import { tokenToId } from "../api/api";

function ProductCard({ product, onFavoriteAdded }) {
  const handleAddFavorite = async () => {
    try {
      const userId = await tokenToId();
      console.log("User ID from token:", userId);

      await addFavoriteProduct(userId, product.productID);
      console.log("Favorite product added:", product.productID);

      onFavoriteAdded(`${product.productName} added to favorites!`, "success");
    } catch (error) {
      const message = error.message || "Error adding to favorites!";
      console.error("An error occurred:", message);
      onFavoriteAdded(message, "error");
    }
  };

  return (
    <div className="card h-100 border-0 shadow-sm product-card">
      <div className="position-relative overflow-hidden">
        <img
          src={product.imageUrl}
          className="card-img-top object-fit-fill rounded fs-6"
          style={{ height: "300px", width: "150px", objectFit: "contain" }}
          alt={product.productName}
        />

        <div className="card-overlay position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center">
          <Link
            to={`/productDetail/${product.productID}`}
            className="btn btn-light btn-sm me-2 overlay-btn"
          >
            <i className="fas fa-eye"></i> View
          </Link>

          <button
            onClick={handleAddFavorite}
            className="btn btn-light btn-sm overlay-btn"
          >
            <i className="fa-regular fa-heart"></i>
          </button>
        </div>
      </div>

      <div className="card-body d-flex flex-column">
        <h5 className="card-title fw-bold product-name">
          {product.productName}
        </h5>
      </div>
    </div>
  );
}

export default ProductCard;