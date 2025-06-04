import React from "react";
import { Link } from "react-router-dom";
import { removeFavoriteProduct, tokenToId } from "../api/api";

function FavoriteProductCard({
  productID,
  title,
  description,
  price,
  imageUrl,
  onFavoriteRemoved,
}) {
  const handleRemoveFavorite = async () => {
    try {
      const userId = await tokenToId();
      await removeFavoriteProduct(userId, productID);
      onFavoriteRemoved("Product removed from favorites!", "danger");
    } catch (error) {
      console.error(error.message);
      onFavoriteRemoved("Error removing from favorites!", "warning");
    }
  };

  return (
    <div className="card h-100 border-0 shadow-sm product-card">
      <div className="position-relative overflow-hidden">
        <img
          src={"https://placehold.co/600x400"}
          className="card-img-top"
          style={{ height: "250px", objectFit: "cover" }}
          alt={title}
        />

        <div className="card-overlay position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center">
          <Link
            to={`/productDetail/${productID}`}
            className="btn btn-light btn-sm me-2 overlay-btn"
          >
            <i className="fas fa-eye"></i> View
          </Link>

          <button
            onClick={handleRemoveFavorite}
            className="btn btn-danger btn-sm overlay-btn"
          >
            <i className="fas fa-heart"></i>
          </button>
        </div>

        <div className="position-absolute top-0 end-0 m-3">
          <span className="badge bg-primary fs-6 px-3 py-2">₺{price}</span>
        </div>
      </div>

      <div className="card-body d-flex flex-column">
        <h5 className="card-title fw-bold text-truncate" title={title}>
          {title}
        </h5>

        <p
          className="card-text text-muted small flex-grow-1"
          style={{
            overflow: "hidden",
          }}
        >
          {description}
        </p>
      </div>
    </div>
  );
}

export default FavoriteProductCard;
