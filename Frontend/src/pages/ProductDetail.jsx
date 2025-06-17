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
      storage: "Depolama",
      ram: "RAM",
      phone_brand: "Marka",
      phone_model: "Model",
      dimensions: "Boyutlar",
      display_size: "Ekran Boyutu",
      display_resolution: "Ekran Çözünürlüğü",
      os: "İşletim Sistemi",
      battery: "Batarya",
      video: "Video",
      chipset: "Yonga Seti",
      cpu: "İşlemci",
      gpu: "Grafik İşlemci",
      ppi_density: "PPI Yoğunluğu",
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
      <div className="alert alert-info text-center">
        <p>Ürün özellikleri bulunamadı</p>
      </div>
    );
  }

  return (
    <div className="card h-100">
      <div className="card-header bg-primary text-white">
        <h5 className="card-title mb-0">
          <i className="fas fa-info-circle me-2"></i>
          Ürün Özellikleri
        </h5>
      </div>
      <div className="card-body p-0">
        <table className="table table-striped table-hover mb-0">
          <tbody>
            {specs.map((spec, index) => (
              <tr key={index}>
                <td className="fw-medium text-muted" style={{ width: "40%" }}>
                  {formatKey(spec.key)}
                </td>
                <td className="fw-bold">{formatValue(spec.key, spec.value)}</td>
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

  const todayDate = getTodayDate();
  const chartData = createChartData(forecastData, todayDate, addDaysToDate);
  const chartOptions = createChartOptions();
  const stats = calculateStats(forecastData);

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
          <p className="text-gray-600 mt-4">Ürün yükleniyor...</p>
        </div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-600 text-lg">Ürün bulunamadı!</p>
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
            <h5 className="fw-semibold mb-3">📈 15 Günlük Fiyat Tahmini</h5>

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
                  <p className="text-muted">Tahmin hesaplanıyor...</p>
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
                <p className="mb-2">Tahmin bulunamadı!</p>
                <button
                  onClick={handleRefreshForecast}
                  className="btn btn-primary"
                >
                  Tekrar Dene
                </button>
              </div>
            )}
          </div>
        </div>

        <div className="col-lg-4">
          <div className="bg-white rounded shadow-sm p-4 h-100">
            <h5 className="fw-semibold mb-3">📊 Fiyat İstatistikleri</h5>

            {stats && forecastData.length > 0 ? (
              <div className="row g-3">
                <div className="col-sm-6">
                  <div className="bg-success bg-opacity-10 border border-success rounded p-3">
                    <div className="h4 text-success fw-bold mb-1">
                      {stats.min.toLocaleString("tr-TR", {
                        style: "currency",
                        currency: "TRY",
                        minimumFractionDigits: 0,
                      })}
                    </div>
                    <div className="small text-success">En Düşük Fiyat</div>
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
                    <div className="small text-danger">En Yüksek Fiyat</div>
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
                    <div className="small text-primary">Ortalama Fiyat</div>
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
                    <div className="small">Fiyat Trendi</div>
                  </div>
                </div>
              </div>
            ) : (
              <div
                className="text-center text-muted"
                style={{ height: "100px" }}
              >
                <div className="fs-2">📉</div>
                <p>İstatistik verisi yok</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProductDetail;
