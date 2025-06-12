import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { api, getProductById, predict_lstm } from "../api/api";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const DescriptionTable = ({ description }) => {
  const parseDescription = (desc) => {
    if (!desc) return [];

    const pairs = desc.split(";");
    return pairs
      .map((pair) => {
        const [key, value] = pair.split(":");
        return {
          key: key?.trim(),
          value: value?.trim(),
        };
      })
      .filter((item) => item.key && item.value);
  };

  const formatKey = (key) => {
    const keyMap = {
      storage: "Storage",
      ram: "RAM",
      phone_brand: "Brand",
      phone_model: "Phone Model",
      dimensions: "Dimensions",
      display_size: "Display Size",
      display_resolution: "Display Resolution",
      os: "Operating System",
      battery: "Battery",
      video: "Video",
      chipset: "Chipset",
      cpu: "Processor",
      gpu: "Graphics Processor",
      ppi_density: "PPI Density",
    };

    return (
      keyMap[key] ||
      key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase())
    );
  };

  const formatValue = (key, value) => {
    switch (key) {
      case "storage":
        return `${value} GB`;
      case "ram":
        return `${value} GB`;
      case "display_size":
        return `${value}"`;
      case "battery":
        return `${value} mAh`;
      case "ppi_density":
        return `${value} PPI`;
      default:
        return value;
    }
  };

  const specs = parseDescription(description);

  if (specs.length === 0) {
    return (
      <div className="bg-gray-50 rounded-lg p-4">
        <p className="text-gray-500 text-center">Product features not found</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border shadow-sm">
      <div className="px-4 py-3 border-b bg-gray-50">
        <h3 className="text-lg font-semibold text-gray-900">
          Product Features
        </h3>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <tbody className="divide-y divide-gray-200">
            {specs.map((spec, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-4 py-3 text-sm font-medium text-gray-600 w-1/3">
                  {formatKey(spec.key)}
                </td>
                <td className="px-4 py-3 text-sm text-gray-900">
                  <div className="break-words">
                    {formatValue(spec.key, spec.value)}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

function ProductDetail() {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [forecastData, setForecastData] = useState([]);
  const [forecastLoading, setForecastLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await getProductById(id);
        setProduct(data);
        console.log("Product details:", data.productName);
      } catch (error) {
        console.error("Failed to fetch product details:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchProduct();
  }, [id]);

  const fetchForecastData = async (productName) => {
    if (!productName || !productName.trim()) {
      console.warn("Product name is empty, can't get prediction data");
      return;
    }

    setForecastLoading(true);
    setError(null);

    try {
      const response = await predict_lstm(product.productName);
      setForecastData(response.forecast);
    } catch (error) {
      console.error("Failed to fetch forecast data:", error);
    } finally {
      setForecastLoading(false);
    }
  };

  const handleRefreshForecast = async () => {
    if (product && product.productName) {
      await fetchForecastData(product.productName);
    }
  };

  const chartData = {
    labels: forecastData.map((_, index) => `${index + 1}. Gün`),
    datasets: [
      {
        label: "Estimated price (₺)",
        data: forecastData,
        borderColor: "rgb(59, 130, 246)",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "rgb(59, 130, 246)",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        pointHoverBackgroundColor: "rgb(37, 99, 235)",
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 1000,
      easing: "easeInOutQuart",
    },
    interaction: {
      intersect: false,
      mode: "index",
    },
    scales: {
      y: {
        beginAtZero: false,
        grid: {
          color: "rgba(0, 0, 0, 0.1)",
        },
        ticks: {
          callback: function (value) {
            return new Intl.NumberFormat("tr-TR", {
              style: "currency",
              currency: "TRY",
              minimumFractionDigits: 0,
            }).format(value);
          },
        },
      },
      x: {
        grid: {
          color: "rgba(0, 0, 0, 0.1)",
        },
      },
    },
    plugins: {
      tooltip: {
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        titleColor: "#fff",
        bodyColor: "#fff",
        borderColor: "rgb(59, 130, 246)",
        borderWidth: 1,
        cornerRadius: 8,
        callbacks: {
          label: function (context) {
            return `Estimated Price: ${new Intl.NumberFormat("tr-TR", {
              style: "currency",
              currency: "TRY",
            }).format(context.parsed.y)}`;
          },
        },
      },
      legend: {
        display: false,
      },
    },
  };

  const getStats = () => {
    if (!forecastData.length) return null;

    const min = Math.min(...forecastData);
    const max = Math.max(...forecastData);
    const avg = forecastData.reduce((a, b) => a + b, 0) / forecastData.length;
    const trend = forecastData[forecastData.length - 1] - forecastData[0];
    const trendPercent = ((trend / forecastData[0]) * 100).toFixed(1);

    return { min, max, avg, trend, trendPercent };
  };

  const stats = getStats();

  useEffect(() => {
    if (product && product.productName && forecastData.length === 0) {
      fetchForecastData(product.productName);
    }
  }, [product]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-600 mt-4">Product loading...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600 text-lg">Product not found!</p>
      </div>
    );
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
                  📈 Min price for 15 days
                </p>
              </div>
            </div>
          </div>

          <div className="p-8 pt-4">
            <DescriptionTable description={product.description} />
          </div>

          <div className="bg-blue-50 border border-blue-200 rounded-lg p-5 m-8 mt-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">
                📊 Price Prediction for 15 days
              </h3>
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
                <p className="text-sm">{error}</p>
              </div>
            )}

            {forecastLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="text-center">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500 mx-auto"></div>
                  <p className="text-gray-600 mt-2">Calculating forecast...</p>
                </div>
              </div>
            ) : forecastData.length > 0 ? (
              <>
                <div className="h-80 mb-4">
                  <Line data={chartData} options={chartOptions} />
                </div>

                {stats && (
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4">
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-lg font-bold text-green-600">
                        {stats.min.toLocaleString("tr-TR", {
                          style: "currency",
                          currency: "TRY",
                          minimumFractionDigits: 0,
                        })}
                      </div>
                      <div className="text-xs text-gray-600">Min Price</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-lg font-bold text-red-600">
                        {stats.max.toLocaleString("tr-TR", {
                          style: "currency",
                          currency: "TRY",
                          minimumFractionDigits: 0,
                        })}
                      </div>
                      <div className="text-xs text-gray-600">Max Price</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div className="text-lg font-bold text-blue-600">
                        {stats.avg.toLocaleString("tr-TR", {
                          style: "currency",
                          currency: "TRY",
                          minimumFractionDigits: 0,
                        })}
                      </div>
                      <div className="text-xs text-gray-600">Average</div>
                    </div>
                    <div className="bg-white rounded-lg p-3 text-center">
                      <div
                        className={`text-lg font-bold ${
                          stats.trend > 0
                            ? "text-green-600"
                            : stats.trend < 0
                            ? "text-red-600"
                            : "text-gray-600"
                        }`}
                      >
                        {stats.trend > 0 ? "📈" : stats.trend < 0 ? "📉" : "➡️"}{" "}
                        {stats.trendPercent}%
                      </div>
                      <div className="text-xs text-gray-600">Trend</div>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="flex items-center justify-center h-64">
                <div className="text-center text-gray-500">
                  <p className="text-lg">📊</p>
                  <p>Prediction not found!</p>
                  <button
                    onClick={handleRefreshForecast}
                    className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
