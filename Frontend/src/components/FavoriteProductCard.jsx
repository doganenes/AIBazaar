import React from "react";
import { Link } from "react-router-dom";
import { getProductById } from "../api/api";

function FavoriteProductCard({ productID, title, description, imageUrl }) {
  return (
    <div className="card mt-3" style={{ width: "100%" }}>
      <img
        src={imageUrl}
        className="card-img-top"
        alt={title}
        style={{ objectFit: "cover", height: "200px" }}
      />
      <div className="card-body">
        <h5 className="card-title">{title}</h5>
        <p className="card-text">{description}</p>
        <Link
          to={`/productDetail/${productID}`}
          className="btn btn-primary"
        >
          Detail
        </Link>
      </div>
    </div>
  );
}

export default FavoriteProductCard;
