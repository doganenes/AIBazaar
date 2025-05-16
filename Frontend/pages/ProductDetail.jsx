import React from "react";

function ProductDetail() {
  return (
    <div className="container mt-5">
      <div className="row">
        <div className="col-md-6 text-center">
          <img
            src="project.jpg"
            alt="iPhone 15 128 GB Siyah"
            className="img-fluid rounded"
          />
        </div>

        <div className="col-md-6">
          <h3 className="mb-3">Apple iPhone 15 128 GB Siyah</h3>
          <p className="text-muted">⭐⭐⭐⭐⭐</p>
          <h4 className="text-success">53.999,00 TL</h4>
          <p className="text-danger">30 günün en düşük fiyatı</p>
          <div className="mb-2">
            <strong>Renk:</strong> Siyah
          </div>
          <div className="mb-2">
            <strong>Kapasite:</strong> 128 GB
          </div>
          <div className="mb-2">
            <p>Fiyat değişimi burada olacak</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
