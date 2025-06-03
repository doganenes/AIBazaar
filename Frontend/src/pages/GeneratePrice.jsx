import React, { useState } from "react";
import axios from "axios";
import "../css/GeneratePrice.css";
function GeneratePrice() {
  const [formData, setFormData] = useState({
    ram: "",
    storage: "",
    display_size: "",
    battery: "",
    foldable: "",
    ppi: "",
    os: "",
    display_type: "",
    video_resolution: "",
    chipset: "",
  });

  const [predictedPrice, setPredictedPrice] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [formErrors, setFormErrors] = useState({});

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

  const validateForm = () => {
    const errors = {};
    const requiredFields = [
      "ram",
      "storage",
      "display_size",
      "battery",
      "foldable",
      "ppi",
      "os",
      "display_type",
      "video_resolution",
      "chipset",
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
      const response = await axios.post(
        "http://localhost:8000/api/predict_product_xgboost/",
        formData
      );
      console.log("Backend response:", response.data);
      setPredictedPrice(response.data.price);
      setIsLoading(false);
    } catch (error) {
      console.error("API request error:", error);
      setPredictedPrice(null);
    }

  };

  const isFormValid = Object.values(formData).every((value) => value !== "");

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-3">
            📱 Smart Phone Price Estimator
          </h1>
          <p className="text-gray-600 text-lg">
            Get instant price estimates based on your product specifications
          </p>
        </div>

        <div className="row g-4">
          <div className="col-lg-8">
            <div className="card shadow-lg border-0 h-100">
              <div className="card-header bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4">
                <h3 className="card-title mb-0 d-flex align-items-center text-dark">
                  <span className="me-3">⚙️</span>
                  Product Specifications
                </h3>
              </div>
              <div className="card-body p-4">
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">💾</span>Storage
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.storage ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.storage ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="storage"
                      value={formData.storage}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.storage
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
                    {formErrors.storage && (
                      <div className="invalid-feedback">
                        {formErrors.storage}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🧠</span>RAM
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.ram ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.ram ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="ram"
                      value={formData.ram}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.ram
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
                    {formErrors.ram && (
                      <div className="invalid-feedback">{formErrors.ram}</div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">📐</span>Display Size
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.display_size ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.display_size
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="display_size"
                      value={formData.display_size}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.display_size
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Display Size</option>
                      <option value="5.5">5.5 inch</option>
                      <option value="6.1">6.1 inch</option>
                      <option value="6.7">6.7 inch</option>
                    </select>
                    {formErrors.display_size && (
                      <div className="invalid-feedback">
                        {formErrors.display_size}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🤖</span>Operating System
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.os ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.os ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="os"
                      value={formData.os}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.os
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select OS</option>
                      <option value="Android">Android</option>
                      <option value="iOS">iOS</option>
                    </select>
                    {formErrors.os && (
                      <div className="invalid-feedback">{formErrors.os}</div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🔋</span>Battery
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.battery ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.battery ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="battery"
                      value={formData.battery}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.battery
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Battery</option>
                      <option value="3000">3000 mAh</option>
                      <option value="4000">4000 mAh</option>
                      <option value="5000">5000 mAh</option>
                    </select>
                    {formErrors.battery && (
                      <div className="invalid-feedback">
                        {formErrors.battery}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">📱</span>Foldable
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.foldable ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.foldable
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="foldable"
                      value={formData.foldable}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.foldable
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Foldable Status</option>
                      <option value="1">Yes</option>
                      <option value="0">No</option>
                    </select>
                    {formErrors.foldable && (
                      <div className="invalid-feedback">
                        {formErrors.foldable}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🖥️</span>Display Type
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.display_type ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.display_type
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="display_type"
                      value={formData.display_type}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.display_type
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Display Type</option>
                      <option value="Amoled">AMOLED</option>
                      <option value="Super AMOLED">Super AMOLED</option>
                      <option value="Dynamic AMOLED">Dynamic AMOLED</option>
                      <option value="LCD">LCD</option>
                      <option value="Super Retina">Super Retina</option>
                      <option value="IPS LCD">IPS LCD</option>
                      <option value="OLED">OLED</option>
                      <option value="Liquid Retina">Liquid Retina</option>
                    </select>
                    {formErrors.display_type && (
                      <div className="invalid-feedback">
                        {formErrors.display_type}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🎥</span>Video Resolution
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.video_resolution ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.video_resolution
                          ? "#dc3545"
                          : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="video_resolution"
                      value={formData.video_resolution}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor =
                          formErrors.video_resolution ? "#dc3545" : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Video Resolution</option>
                      <option value="1080p">1080p</option>
                      <option value="4K">4K</option>
                      <option value="8K">8K</option>
                    </select>
                    {formErrors.video_resolution && (
                      <div className="invalid-feedback">
                        {formErrors.video_resolution}
                      </div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">🔍</span>PPI (Pixels per inch)
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.ppi ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.ppi ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="ppi"
                      value={formData.ppi}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.ppi
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select PPI Range</option>
                      <option value="1">250 - 350</option>
                      <option value="2">350 - 450</option>
                      <option value="3">450 - 500</option>
                      <option value="4">500+</option>
                    </select>
                    {formErrors.ppi && (
                      <div className="invalid-feedback">{formErrors.ppi}</div>
                    )}
                  </div>

                  <div className="col-md-6">
                    <label className="form-label fw-semibold text-gray-700">
                      <span className="me-2">⚡</span>Chipset Lithography (nm)
                    </label>
                    <select
                      className={`form-select form-select-lg border-2 ${
                        formErrors.chipset ? "is-invalid" : ""
                      }`}
                      style={{
                        borderColor: formErrors.chipset ? "#dc3545" : "#e5e7eb",
                        transition: "all 0.3s",
                      }}
                      name="chipset"
                      value={formData.chipset}
                      onChange={handleChange}
                      onFocus={(e) => (e.target.style.borderColor = "#3b82f6")}
                      onBlur={(e) =>
                        (e.target.style.borderColor = formErrors.chipset
                          ? "#dc3545"
                          : "#e5e7eb")
                      }
                      required
                    >
                      <option value="">Select Chipset nm</option>
                      <option value="3">3nm</option>
                      <option value="4">4nm</option>
                      <option value="5">5nm</option>
                      <option value="6">6nm</option>
                      <option value="7">7nm</option>
                      <option value="8">8nm</option>
                      <option value="9">9nm</option>
                      <option value="10">10nm</option>
                    </select>
                    {formErrors.chipset && (
                      <div className="invalid-feedback">
                        {formErrors.chipset}
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

          <div className="col-lg-4">
            <div className="card shadow-lg border-0 h-100">
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
                      <div className="display-3 fw-bold mb-2">
                        ${predictedPrice.toFixed(2)}
                      </div>
                      <small className="opacity-75">USD</small>
                    </div>

                    <div
                      className="alert alert-info border-0 mb-4"
                      style={{
                        backgroundColor: "#f8f9ff",
                        color: "#4c63d2",
                      }}
                    >
                      <small>
                        This estimate is based on the specifications you
                        provided and current market trends.
                      </small>
                    </div>

                    <div className="row g-2 text-sm">
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">Market Analysis</span>
                          <span className="text-success fw-semibold">
                            ✓ Complete
                          </span>
                        </div>
                      </div>
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">Spec Comparison</span>
                          <span className="text-success fw-semibold">
                            ✓ Complete
                          </span>
                        </div>
                      </div>
                      <div className="col-12">
                        <div className="d-flex justify-content-between align-items-center py-2 px-3 bg-light rounded">
                          <span className="text-muted">Price Calculation</span>
                          <span className="text-success fw-semibold">
                            ✓ Complete
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center text-muted">
                    <div style={{ fontSize: "4rem" }} className="mb-3">
                      📊
                    </div>
                    <h5 className="fw-light mb-3">
                      Ready to calculate your product price
                    </h5>
                    <p className="small">
                      Fill out all the fields to get your price estimation
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
