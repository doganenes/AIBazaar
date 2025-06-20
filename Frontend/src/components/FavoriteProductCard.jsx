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
      onFavoriteRemoved(`${title} removed from favorites!`, "success");
    } catch (error) {
      console.error(error.message);
      onFavoriteRemoved("Error removing from favorites!", "danger");
    }
  };

  return (
    <div className="card h-100 border-0 shadow-sm product-card">
      <div className="position-relative overflow-hidden">
        <img
          src={imageUrl}
          className="card-img-top"
          style={{ height: "250px",width:"150px", objectFit: "contain" }}
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
            className="btn btn-light btn-sm overlay-btn"
          >
            <i class="fa-solid fa-heart text-danger"></i>
          </button>
        </div>
      </div>

      <div className="card-body d-flex flex-column">
        <h5 className="card-title fw-bold text-truncate" title={title}>
          {title}
        </h5>
      </div>
    </div>
  );
}

export default FavoriteProductCard;