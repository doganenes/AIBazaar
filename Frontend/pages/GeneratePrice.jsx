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
    chipset: ""
  });

  const [predictedPrice, setPredictedPrice] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post(
        "http://localhost:8000/api/predict_product_knn/",
        formData
      );
      console.log("Backend response:", response.data);
      setPredictedPrice(response.data.price);
    } catch (error) {
      console.error("API request error:", error);
      setPredictedPrice(null);
    }
  };
  return (
    <div className="container generatePriceContainer my-5">
      <div className="row justify-content-center g-4 mt-5">
        <div className="col-12 col-md-5 mb-4 mt-5 bg-secondary rounded ms-md-4">
          <form onSubmit={handleSubmit} className="mt-5">
            <h3 className="text-light">Price estimate for features</h3>

            <div className="mb-3">
              <label className="form-label">Storage</label>
              <select
                className="form-select"
                name="storage"
                value={formData.storage}
                onChange={handleChange}
                required
              >
                <option value="">Select Storage</option>
                <option value="64">64 GB</option>
                <option value="128">128 GB</option>
                <option value="256">256 GB</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">RAM</label>
              <select
                className="form-select"
                name="ram"
                value={formData.ram}
                onChange={handleChange}
                required
              >
                <option value="">Select RAM</option>
                <option value="4">4 GB</option>
                <option value="6">6 GB</option>
                <option value="8">8 GB</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">Display Size</label>
              <select
                className="form-select"
                name="display_size"
                value={formData.display_size}
                onChange={handleChange}
                required
              >
                <option value="">Select Display</option>
                <option value="5.5">5.5 inch</option>
                <option value="6.1">6.1 inch</option>
                <option value="6.7">6.7 inch</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">OS</label>
              <select
                className="form-select"
                name="os"
                value={formData.os}
                onChange={handleChange}
                required
              >
                <option value="">Select OS</option>
                <option value="Android">Android</option>
                <option value="iOS">iOS</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">Battery</label>
              <select
                className="form-select"
                name="battery"
                value={formData.battery}
                onChange={handleChange}
                required
              >
                <option value="">Select Battery</option>
                <option value="3000">3000 mAh</option>
                <option value="4000">4000 mAh</option>
                <option value="5000">5000 mAh</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">Foldable</label>
              <select
                className="form-select"
                name="foldable"
                value={formData.foldable}
                onChange={handleChange}
                required
              >
                <option value="">Select Foldable Status</option>
                <option value="1">True</option>
                <option value="0">False</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">Display Type</label>
              <select
                className="form-select"
                name="display_type"
                value={formData.display_type}
                onChange={handleChange}
                required
              >
                <option value="">Select Display Type</option>
                <option value="Amoled">Amoled</option>
                <option value="Super AMOLED">Super Amoled</option>
                <option value="Dynamic AMOLED">Dynamic Amoled</option>
                <option value="LCD">LCD</option>
                <option value="Super Retina">Super Retina</option>
                <option value="IPS LCD">LCD</option>
                <option value="OLED">OLED</option>
                <option value="Liquid Retina">Liquid Retina</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">Video Resolution</label>
              <select
                className="form-select"
                name="video_resolution"
                value={formData.video_resolution}
                onChange={handleChange}
                required
              >
                <option value="">Select Video Resolution</option>
                <option value="1080p">1080p</option>
                <option value="4K">4K</option>
                <option value="8K">8K</option>
              </select>
            </div>

            <div className="mb-3">
              <label className="form-label">PPI</label>
              <select
                className="form-select"
                name="ppi"
                value={formData.ppi}
                onChange={handleChange}
                required
              >
                <option value="">Select PPI (Pixels per inch)</option>
                <option value="1">250 - 350</option>
                <option value="2">350 - 450</option>
                <option value="3">450 - 500</option>
                <option value="4">500+</option>
              </select>
            </div>
            <div className="mb-3">
              <label className="form-label">Chipset Litography</label>
              <select
                className="form-select"
                name="chipset"
                value={formData.chipset}
                onChange={handleChange}
                required
              >
                <option value="">Select chipset nm</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
                <option value="6">6</option>
                <option value="7">7</option>
                <option value="8">8</option>
                <option value="9">9</option>
                <option value="10">10</option>
              </select>
            </div>

            <button type="submit" className="btn btn-primary mb-3">
              Submit
            </button>
            {predictedPrice !== null && (
              <p className="mt-3 text-light fw-bold">
                Estimated Price: {predictedPrice} USD
              </p>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default GeneratePrice;
