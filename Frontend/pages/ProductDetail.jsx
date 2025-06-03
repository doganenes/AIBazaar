import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

function ProductDetail() {
  const { id } = useParams();

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`https://localhost:7011/api/Product/getProductById/${id}`)
      .then((response) => {
        setProduct(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Ürün detayları alınamadı:", error);
        setLoading(false);
      });
  }, [id]);

  if (loading) {
    return <p className="text-center mt-10">Loading...</p>;
  }

  return (
    <div className="min-h-screen py-10 mt-5">
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white rounded-2xl shadow-md overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
            <div className="flex justify-center items-center">
              <img
                src={`${product.imageUrl}`}
                alt={product.productName}
                className="w-full max-w-sm mt-5 mb-3 h-auto rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300"
              />
            </div>

            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-semibold text-gray-900">
                  {product.productName}
                </h1>
              </div>

              <div className="bg-green-50 rounded-lg p-5">
                <h2 className="text-3xl font-bold text-green-600">
                  {product.price.toLocaleString("tr-TR", {
                    style: "currency",
                    currency: "TRY",
                  })}
                </h2>
                <p className="text-sm text-red-600 font-medium mt-1 flex items-center">
                  📈 30 günün en düşük fiyatı
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between border-b pb-2">
                  <span className="text-gray-600 font-medium">Açıklama:</span>
                  <span className="text-gray-900">{product.description}</span>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-5 mt-4">
                <h3 className="text-base font-semibold text-gray-800 mb-3">
                  Fiyat değişimi burada olacak
                </h3>
                <div className="flex justify-center">
                  <img
                    src="/graphic.jpg"
                    alt="Fiyat Grafiği"
                    className="rounded-md shadow-sm"
                    style={{ width: "100%", maxWidth: "400px" }}
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
