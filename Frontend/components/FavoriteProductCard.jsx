import React from "react";

function FavoriteProductCard({ title, description, imageUrl }) {
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
        <a href="/productdetail" className="btn btn-primary">
          Detail
        </a>
      </div>
    </div>
  );
}

export default FavoriteProductCard;
