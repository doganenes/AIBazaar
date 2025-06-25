import React, { useEffect, useState, useRef } from "react";
import { useParams } from "react-router-dom";
import { api, getProductById, predict_lstm } from "../api/api";
import { getTodayDate, addDaysToDate } from "../utils/dateUtils";
import {
  createChartData,
  createChartOptions,
  calculateStats,
} from "../utils/chartUtils";
import {
  translateDescription,
  formatValue,
  getDisplayLabel,
} from "../utils/keyUtils";
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

import { capitalizeEachWord } from "../utils/detailUtils";
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
  const specs = translateDescription(description);

  if (specs.length === 0) {
    return (
      <div className="alert alert-info text-center">
        <p>Features not found!</p>
      </div>
    );
  }

  return (
    <div className="card h-100">
      <div
        className="card-header text-white"
        style={{
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        }}
      >
        <h5 className="card-title mb-0">
          <i className="fas fa-list-ul me-2 p-2"></i>
          Features
        </h5>
      </div>
      <div className="card-body p-0">
        <table className="table table-bordered table-hover mb-0">
          <tbody>
            {specs.map(({ key, value }, index) => (
              <tr key={index}>
                <td className="fw-medium text-muted" style={{ width: "40%" }}>
                  {getDisplayLabel(key)}
                </td>
                <td className="fw-bold">{formatValue(key, value)}</td>
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
  console.log("Product ID from URL:", id);
  const [productId, setProductId] = useState(id);
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

  const fetchForecastData = async (productId) => {
    if (!productId) {
      console.warn("Product ID is empty, can't get prediction data");
      return;
    }

    setForecastLoading(true);
    setError(null);

    try {
      const response = await predict_lstm(productId);
      console.log("API Response:", response);

      if (response && response.predicted_prices) {
        setForecastData(response.predicted_prices);
      } else {
        setError("Forecast not found for this product");
        setForecastData([]);
      }
    } catch (error) {
      console.error("Failed to fetch forecast data:", error);
      setError("Error occurred while fetching forecast data");
      setForecastData([]);
    } finally {
      setForecastLoading(false);
    }
  };

  const handleRefreshForecast = async () => {
    if (product && productId) {
      await fetchForecastData(productId);
    }
  };

  const todayDate = getTodayDate();
  const chartData = createChartData(forecastData, todayDate, addDaysToDate);
  const chartOptions = createChartOptions();
  const stats = calculateStats(forecastData);

  useEffect(() => {
    if (product && productId && forecastData.length === 0) {
      fetchForecastData(productId);
    }
  }, [product]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-600 mt-4">Loading product...</p>
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
    <div className="container mt-5 py-5 min-vh-100 bg-light">
      <div className="bg-white rounded shadow-sm p-4 mb-4">
        <h1 className="h3 fw-bold mb-2">{product.productName}</h1>
      </div>

      <div className="row g-4 mb-4">
        <div className="col-lg-6">
          <div className="bg-white rounded shadow-sm p-4 h-100 d-flex justify-content-center align-items-center">
            <img
              src={product.imageUrl}
              alt={product.productName}
              className="img-fluid rounded shadow-sm"
              style={{ maxHeight: "400px", objectFit: "contain" }}
            />
          </div>
        </div>

        <div className="col-lg-6">
          <div className="bg-white rounded shadow-sm p-4 h-100">
            <DescriptionTable description={product.description} />
          </div>
        </div>
      </div>

      <div className="row g-4">
        <div className="col-lg-8">
          <div className="bg-white rounded shadow-sm p-4 h-100">
            <h5 className="fw-semibold mb-3">
              📈 Price Forecast for {product.productName} in 15 Days
            </h5>

            {error && <div className="alert alert-danger small">{error}</div>}

            {forecastLoading ? (
              <div
                className="d-flex justify-content-center align-items-center"
                style={{ height: "300px" }}
              >
                <div className="text-center">
                  <div
                    className="spinner-border text-primary mb-3"
                    role="status"
                  ></div>
                  <p className="text-muted">Loading graph...</p>
                </div>
              </div>
            ) : forecastData.length > 0 ? (
              <div style={{ height: "300px" }}>
                <Line data={chartData} options={chartOptions} />
              </div>
            ) : (
              <div
                className="text-center text-muted"
                style={{ height: "300px" }}
              >
                <div className="fs-1">📊</div>
                <p className="mb-2">Forecast not found!</p>
                <button
                  onClick={handleRefreshForecast}
                  className="btn btn-primary"
                >
                  Try Again
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="col-lg-4">
          <div className="bg-white rounded shadow-sm p-4 h-100">
            <h5 className="fw-semibold mb-5">📊 Price Statistics</h5>

            {forecastLoading ? (
              <div
                className="d-flex justify-content-center align-items-center"
                style={{ height: "200px" }}
              >
                <div className="text-center">
                  <div
                    className="spinner-border text-primary mb-3"
                    role="status"
                  ></div>
                  <p className="text-muted">Loading stats...</p>
                </div>
              </div>
            ) : stats && forecastData.length > 0 ? (
              <div className="row g-3 mt-5">
                <div className="col-sm-6">
                  <div className="bg-success bg-opacity-10 border border-success rounded p-3">
                    <div className="h4 text-success fw-bold mb-1">
                      {stats.min.toLocaleString("tr-TR", {
                        style: "currency",
                        currency: "TRY",
                        minimumFractionDigits: 0,
                      })}
                    </div>
                    <div className="small text-success">Min Price</div>
                  </div>
                </div>

                <div className="col-sm-6">
                  <div className="bg-danger bg-opacity-10 border border-danger rounded p-3">
                    <div className="h4 text-danger fw-bold mb-1">
                      {stats.max.toLocaleString("tr-TR", {
                        style: "currency",
                        currency: "TRY",
                        minimumFractionDigits: 0,
                      })}
                    </div>
                    <div className="small text-danger">Max Price</div>
                  </div>
                </div>

                <div className="col-sm-6">
                  <div className="bg-primary bg-opacity-10 border border-primary rounded p-3">
                    <div className="h4 text-primary fw-bold mb-1">
                      {stats.avg.toLocaleString("tr-TR", {
                        style: "currency",
                        currency: "TRY",
                        minimumFractionDigits: 0,
                      })}
                    </div>
                    <div className="small text-primary">Average</div>
                  </div>
                </div>

                <div className="col-sm-6">
                  <div
                    className={`border rounded p-3 ${
                      stats.trend > 0
                        ? "bg-success bg-opacity-10 border-success"
                        : stats.trend < 0
                        ? "bg-danger bg-opacity-10 border-danger"
                        : "bg-secondary bg-opacity-10 border-secondary"
                    }`}
                  >
                    <div
                      className={`h4 fw-bold mb-1 ${
                        stats.trend > 0
                          ? "text-success"
                          : stats.trend < 0
                          ? "text-danger"
                          : "text-secondary"
                      }`}
                    >
                      {stats.trend > 0 ? "📈" : stats.trend < 0 ? "📉" : "➡️"}{" "}
                      {stats.trendPercent}%
                    </div>
                    <div
                      className={`small ${
                        stats.trend > 0
                          ? "text-success"
                          : stats.trend < 0
                          ? "text-danger"
                          : "text-secondary"
                      }`}
                    >
                      Trend
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div
                className="text-center text-muted"
                style={{ height: "100px" }}
              >
                <div className="fs-2">📉</div>
                <p>Stats not found</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
