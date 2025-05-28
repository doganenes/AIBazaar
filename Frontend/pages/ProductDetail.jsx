import React from "react";

function ProductDetail() {
  return (
    <div className="min-h-screen py-10 mt-5">
      <div className="max-w-5xl mx-auto px-4">
        <div className="bg-white rounded-2xl shadow-md overflow-hidden">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 p-8">
            <div className="flex justify-center items-center">
              <img
                src="https://placehold.co/600x400"
                alt="iPhone 15 128 GB Siyah"
                className="w-full max-w-sm mt-5 mb-3 h-auto rounded-xl shadow-sm hover:shadow-md transition-shadow duration-300"
              />
            </div>

            <div className="space-y-6">
              <div>
                <h1 className="text-3xl font-semibold text-gray-900">
                  Apple iPhone 15 128 GB Siyah
                </h1>
              </div>

              <div className="bg-green-50 rounded-lg p-5">
                <h2 className="text-3xl font-bold text-green-600">
                  53.999,00 TL
                </h2>
                <p className="text-sm text-red-600 font-medium mt-1 flex items-center">
                  📈 30 günün en düşük fiyatı
                </p>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between border-b pb-2">
                  <span className="text-gray-600 font-medium">Renk:</span>
                  <span className="text-gray-900">Siyah</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600 font-medium">Kapasite:</span>
                  <span className="text-gray-900">128 GB</span>
                </div>
              </div>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-5 mt-4">
                <h3 className="text-base font-semibold text-gray-800 mb-3">
                  Fiyat değişimi burada olacak
                </h3>
                <div className="flex justify-center">
                  <img
                    src="graphic.jpg"
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
