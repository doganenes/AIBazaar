import React, { useState, useEffect } from "react";
import axios from "axios";
import "../css/GeneratePrice.css";
import { aiApi, predict_xgboost } from "../api/api";
import { useNavigate } from "react-router-dom";

function GeneratePrice() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    RAM: "",
    Storage: "",
    "Display Size": "6.2",
    "Battery Capacity": "5250",
    "Pixel Density": "375",
    "Operating System": "",
    "Display Technology": "",
    camera: "104",
    "CPU Manufacturing": "",
    "5G": "",
    "Refresh Rate": "",
    Waterproof: "6",
    Dustproof: "6",
  });

  const [predictedPrice, setPredictedPrice] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [formErrors, setFormErrors] = useState({});
  const [closestProduct, setClosestProduct] = useState(null);
  const [closestProductId, setClosestProductId] = useState(null);
  const [formattedPrice, setFormattedPrice] = useState("");

  useEffect(() => {
    if (predictedPrice !== null && predictedPrice !== undefined) {
      const formatted =
        new Intl.NumberFormat("tr-TR", {
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        }).format(predictedPrice) + " ₺";

      setFormattedPrice(formatted);
    }
  }, [predictedPrice]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });

    if (formErrors[e.target.name]) {
      setFormErrors({
        ...formErrors,
        [e.target.name]: null,
      });
    }
  };

  const handleClick = (id) => {
    navigate(`/productdetail/${id}`);
  };

  const validateForm = () => {
    const errors = {};
    const requiredFields = [
      "RAM",
      "Storage",
      "Display Size",
      "Battery Capacity",
      "Pixel Density",
      "Operating System",
      "Display Technology",
      "camera",
      "CPU Manufacturing",
      "5G",
      "Refresh Rate",
      "Waterproof",
      "Dustproof",
    ];

    requiredFields.forEach((field) => {
      if (!formData[field]) {
        errors[field] = "This field is required";
      }
    });

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const isValid = validateForm();

    if (!isValid) {
      return;
    }

    setIsLoading(true);

    try {
      console.log("Submitting form data:", formData);
      // Send form data to the backend for prediction
      const response = await predict_xgboost(formData);
      console.log("Backend response:", response.data);
      setPredictedPrice(response.price);
      setClosestProduct(response.closest_product);
      setClosestProductId(response.closest_product_id);
    } catch (error) {
      console.error("API request error:", error);
      setPredictedPrice(null);
      setClosestProduct(null);
    } finally {
      setIsLoading(false);
    }
  };

  const isFormValid = Object.values(formData).every((value) => value !== "");

  return (
    <div className="min-h-screen bg-gray-50 py-8 mt-5">
      <div className="container forecastContainer mx-auto px-4 mt-5">
        <div className="row g-4 mt-5">
          <div className="col-lg-8 mt-5">
            <div className="card shadow-lg border-0 h-100">
              <div className="card-header bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4">
                <h3 className="card-title mb-0 d-flex justify-content-center align-items-center text-dark">
                  <span className="me-2">⚙️</span>
                  Product Specifications
                </h3>
              </div>
              <div className="card-body p-4">
                <div className="row g-4">
                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">💾</span>Storage
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.Storage ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.Storage ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="Storage"
                      value={formData.Storage}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.Storage
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Storage</option>
                      <option value="64">64 GB</option>
                      <option value="128">128 GB</option>
                      <option value="256">256 GB</option>
                      <option value="512">512 GB</option>
                      <option value="1024">1024 GB</option>
                    </select>
                    {formErrors.Storage && (
                      <div className="invalid-feedback">
                        {formErrors.Storage}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">📟</span>RAM
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.RAM ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.RAM ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="RAM"
                      value={formData.RAM}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.RAM
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select RAM</option>
                      <option value="4">4 GB</option>
                      <option value="6">6 GB</option>
                      <option value="8">8 GB</option>
                      <option value="12">12 GB</option>
                      <option value="16">16 GB</option>
                    </select>
                    {formErrors.RAM && (
                      <div className="invalid-feedback">{formErrors.RAM}</div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">📐</span>Display Size
                    </label>
                    <input
                      type="range"
                      className={`form-range border-2 w-100 ${
                        formErrors["Display Size"] ? "is-invalid" : ""
                      }`}
                      min="5.5"
                      max="7.0"
                      step="0.1"
                      name="Display Size"
                      value={formData["Display Size"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors["Display Size"]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      style={{
                        borderColor: formErrors["Display Size"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      required
                    />
                    <div className="d-flex justify-content-between fs-5 fw-bold">
                      <small className="text-muted">5.5"</small>
                      <small className="text-muted fs-5">
                        {formData["Display Size"]}"
                      </small>
                      <small className="text-muted">7.0"</small>
                    </div>
                    {formErrors["Display Size"] && (
                      <div className="invalid-feedback">
                        {formErrors["Display Size"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🤖</span>Operating System
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors["Operating System"] ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors["Operating System"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="Operating System"
                      value={formData["Operating System"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors[
                          "Operating System"
                        ]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select OS</option>
                      <option value="Android">Android</option>
                      <option value="iOS">iOS</option>
                    </select>
                    {formErrors["Operating System"] && (
                      <div className="invalid-feedback">
                        {formErrors["Operating System"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🔋</span>Battery Capacity
                    </label>
                    <input
                      type="range"
                      className={`form-range border-2 w-100 ${
                        formErrors["Display Size"] ? "is-invalid" : ""
                      }`}
                      min="3500"
                      max="7000"
                      step="250"
                      name="Battery Capacity"
                      value={formData["Battery Capacity"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors[
                          "Battery Capacity"
                        ]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      style={{
                        borderColor: formErrors["Battery Capacity"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      required
                    />
                    <div className="d-flex justify-content-between fs-5 fw-bold">
                      <small className="text-muted">3500"</small>
                      <small className="text-muted fs-5">
                        {formData["Battery Capacity"]}"
                      </small>
                      <small className="text-muted">7000"</small>
                    </div>

                    {formErrors["Battery Capacity"] && (
                      <div className="invalid-feedback">
                        {formErrors["Battery Capacity"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">⚡</span>Quick Charge
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors["Quick Charge"] ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors["Quick Charge"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="Quick Charge"
                      value={formData["Quick Charge"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors["Quick Charge"]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Quick Charge</option>
                      <option value="1">Yes</option>
                      <option value="0">No</option>
                    </select>
                    {formErrors["Quick Charge"] && (
                      <div className="invalid-feedback">
                        {formErrors["Quick Charge"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🖥️</span>Display Technology
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors["Display Technology"] ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors["Display Technology"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="Display Technology"
                      value={formData["Display Technology"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors[
                          "Display Technology"
                        ]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Display Technology</option>
                      <option value="IPS LCD">IPS LCD</option>
                      <option value="OLED">OLED</option>
                      <option value="AMOLED">AMOLED</option>
                      <option value="Super AMOLED">Super AMOLED</option>
                      <option value="Dynamic AMOLED">Dynamic AMOLED</option>
                    </select>
                    {formErrors["Display Technology"] && (
                      <div className="invalid-feedback">
                        {formErrors["Display Technology"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">📷</span>Camera (MP)
                    </label>
                    <input
                      type="range"
                      className={`form-range border-2 w-100 ${
                        formErrors.camera ? "is-invalid" : ""
                      }`}
                      min="8"
                      max="200"
                      step="1"
                      name="camera"
                      value={formData.camera}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.camera
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      style={{
                        borderColor: formErrors.camera ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      required
                    />
                    <div className="d-flex justify-content-between fs-5 fw-bold">
                      <small className="text-muted">8 MP</small>
                      <small className="text-muted fs-5">
                        {formData.camera} MP
                      </small>
                      <small className="text-muted">200 MP</small>
                    </div>
                    {formErrors.camera && (
                      <div className="invalid-feedback">
                        {formErrors.camera}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🔍</span>Pixel Density (PPI)
                    </label>
                    <input
                      type="range"
                      className={`form-range border-2 w-100 ${
                        formErrors["Pixel Density"] ? "is-invalid" : ""
                      }`}
                      min="250"
                      max="500"
                      step="25"
                      name="Pixel Density"
                      value={formData["Pixel Density"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors[
                          "Pixel Density"
                        ]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      style={{
                        borderColor: formErrors["Pixel Density"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      required
                    />
                    <div className="d-flex justify-content-between fs-5 fw-bold">
                      <small className="text-muted">250</small>
                      <small className="text-muted fs-5">
                        {formData["Pixel Density"]} PPI
                      </small>
                      <small className="text-muted">500</small>
                    </div>
                    {formErrors["Pixel Density"] && (
                      <div className="invalid-feedback">
                        {formErrors["Pixel Density"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🔲</span>CPU Manufacturing (nm)
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors["CPU Manufacturing"] ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors["CPU Manufacturing"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="CPU Manufacturing"
                      value={formData["CPU Manufacturing"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors[
                          "CPU Manufacturing"
                        ]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select CPU Manufacturing</option>
                      <option value="3">3nm</option>
                      <option value="4">4nm</option>
                      <option value="5">5nm</option>
                      <option value="6">6nm</option>
                      <option value="7">7nm</option>
                      <option value="8">8nm</option>
                      <option value="9">9nm</option>
                      <option value="10">10nm</option>
                    </select>
                    {formErrors["CPU Manufacturing"] && (
                      <div className="invalid-feedback">
                        {formErrors["CPU Manufacturing"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">📶</span>5G
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors["5G"] ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors["5G"] ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="5G"
                      value={formData["5G"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors["5G"]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select 5G Status</option>
                      <option value="1">Yes</option>
                      <option value="0">No</option>
                    </select>
                    {formErrors["5G"] && (
                      <div className="invalid-feedback">{formErrors["5G"]}</div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🔄</span>Refresh Rate
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors["Refresh Rate"] ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors["Refresh Rate"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="Refresh Rate"
                      value={formData["Refresh Rate"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors["Refresh Rate"]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Refresh Rate (Hz)</option>
                      <option value="60">60 Hz</option>
                      <option value="90">90 Hz</option>
                      <option value="120">120 Hz</option>
                      <option value="144">144 Hz</option>
                    </select>
                    {formErrors["Refresh Rate"] && (
                      <div className="invalid-feedback">
                        {formErrors["Refresh Rate"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">💧</span>Waterproof Value
                    </label>
                    <input
                      type="range"
                      className={`form-range border-2 w-100 ${
                        formErrors["Waterproof"] ? "is-invalid" : ""
                      }`}
                      min="3"
                      max="9"
                      step="1"
                      name="Waterproof"
                      value={formData["Waterproof"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors["Waterproof"]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      style={{
                        borderColor: formErrors["Waterproof"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      required
                    />
                    <div className="d-flex justify-content-between fs-5 fw-bold">
                      <small className="text-muted">3</small>
                      <small className="text-muted fs-5">
                        IPX{formData["Waterproof"]}
                      </small>
                      <small className="text-muted">9</small>
                    </div>
                    {formErrors["Waterproof"] && (
                      <div className="invalid-feedback">
                        {formErrors["Waterproof"]}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🏜️</span>DustProof Value
                    </label>
                    <input
                      type="range"
                      className={`form-range border-2 w-100 ${
                        formErrors["Dustproof"] ? "is-invalid" : ""
                      }`}
                      min="3"
                      max="9"
                      step="1"
                      name="Dustproof"
                      value={formData["Dustproof"]}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors["Dustproof"]
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      style={{
                        borderColor: formErrors["Dustproof"]
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      required
                    />
                    <div className="d-flex justify-content-between fs-5 fw-bold">
                      <small className="text-muted">3</small>
                      <small className="text-muted fs-5">
                        IP{formData["Dustproof"]}X
                      </small>
                      <small className="text-muted">9</small>
                    </div>
                    {formErrors["Dustproof"] && (
                      <div className="invalid-feedback">
                        {formErrors["Dustproof"]}
                      </div>
                    )}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-top">
                  <button
                    type="button"
                    onClick={handleSubmit}
                    disabled={isLoading || !isFormValid}
                    className="btn btn-lg w-100 text-white fw-semibold py-3"
                    style={{
                      background:
                        isLoading || !isFormValid
                          ? "linear-gradient(135deg, #cccccc 0%, #999999 100%)"
                          : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                      border: "none",
                      borderRadius: "12px",
                      transition: "all 0.3s ease",
                      transform: isLoading ? "none" : "translateY(0)",
                      boxShadow:
                        isLoading || !isFormValid
                          ? "none"
                          : "0 4px 15px rgba(102, 126, 234, 0.4)",
                      cursor:
                        isLoading || !isFormValid ? "not-allowed" : "pointer",
                    }}
                    onMouseEnter={(e) => {
                      if (!isLoading && isFormValid) {
                        e.target.style.transform = "translateY(-2px)";
                        e.target.style.boxShadow =
                          "0 8px 25px rgba(102, 126, 234, 0.6)";
                      }
                    }}
                    onMouseLeave={(e) => {
                      if (!isLoading && isFormValid) {
                        e.target.style.transform = "translateY(0)";
                        e.target.style.boxShadow =
                          "0 4px 15px rgba(102, 126, 234, 0.4)";
                      }
                    }}
                  >
                    {isLoading ? (
                      <div className="d-flex align-items-center justify-content-center">
                        <div
                          className="spinner-border spinner-border-sm me-2"
                          role="status"
                        >
                          <span className="visually-hidden">Loading...</span>
                        </div>
                        Calculating Price...
                      </div>
                    ) : !isFormValid ? (
                      "Please fill all fields"
                    ) : (
                      <>
                        <span className="me-2">💰</span>
                        Get Price Estimate
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div className="col-lg-4 mt-5">
            <div className="card shadow-lg border-0 mb-4">
              <div className="card-header bg-gradient-to-r from-green-500 to-blue-600 text-white py-4">
                <h3 className="card-title mb-0 d-flex align-items-center text-dark">
                  <span className="me-3">💰</span>
                  Price Estimation
                </h3>
              </div>
              <div className="card-body p-4 d-flex flex-column justify-content-center">
                {predictedPrice !== null ? (
                  <div className="text-center">
                    <div
                      className="p-4 rounded-4 mb-4"
                      style={{
                        background:
                          "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        color: "white",
                      }}
                    >
                      <h4 className="fw-light mb-2">Estimated Price</h4>
                      <div className="display-3 fw-bold mb-3">
                        {formattedPrice}
                      </div>
                    </div>

                    <div className="row g-2 text-sm">
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">
                            <span className="me-2">📊</span>Market Analysis
                          </span>
                          <span className="text-success fw-semibold">
                            ✓ Complete
                          </span>
                        </div>
                      </div>
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">
                            <span className="me-2">🔍</span>Spec Comparison
                          </span>
                          <span className="text-success fw-semibold">
                            ✓ Complete
                          </span>
                        </div>
                      </div>
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">
                            <span className="me-2">💰</span>Price Calculation
                          </span>
                          <span className="text-success fw-semibold">
                            ✓ Complete
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-muted">
                    <div className="mb-3 fs-1">📊</div>
                    <h5 className="fw-light mb-3">
                      Ready to calculate your product price
                    </h5>
                    <p className="small">
                      Fill out all the fields to get your price estimation.
                    </p>
                  </div>
                )}
              </div>
            </div>

            <div className="card shadow-lg border-0">
              <div className="card-header bg-gradient-to-r from-orange-500 to-red-600 text-white py-4">
                <h3 className="card-title mb-0 d-flex align-items-center text-dark">
                  <span className="me-3">📱</span>
                  Most Similar Device
                </h3>
              </div>
              <div className="card-body p-4">
                {closestProduct ? (
                  <div className="text-center">
                    <div
                      className="p-4 rounded-4 mb-3"
                      style={{
                        background:
                          "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
                        color: "white",
                      }}
                    >
                      <div className="mb-3 fs-1">📱</div>
                      <h4 className="fw-light mb-2">Closest Match</h4>
                      <div className="fw-bold fs-4">
                        <a
                          onClick={handleClick(closestProductId)}
                          className="text-white text-decoration-none"
                          style={{
                            textShadow: "0 2px 4px rgba(0,0,0,0.3)",
                          }}
                        >
                          {closestProduct}
                        </a>
                      </div>
                    </div>

                    <div className="row g-2">
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">
                            <span className="me-2">🔗</span>Device Matching
                          </span>
                          <span className="text-success fw-semibold">
                            ✓ Found
                          </span>
                        </div>
                      </div>
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded"></div>
                      </div>
                    </div>
                  </div>
                ) : predictedPrice !== null ? (
                  <div className="text-center text-muted">
                    <div className="mb-3 fs-1">🔍</div>
                    <h5 className="fw-light mb-3">No similar device found</h5>
                    <p className="small">
                      Your configuration is unique! No close matches were found
                      in our database.
                    </p>
                  </div>
                ) : (
                  <div className="text-center text-muted">
                    <div className="mb-3 fs-1">📱</div>
                    <h5 className="fw-light mb-3">
                      Similar device will appear here
                    </h5>
                    <p className="small">
                      After price calculation, we'll show you the most similar
                      device in our database.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default GeneratePrice;
