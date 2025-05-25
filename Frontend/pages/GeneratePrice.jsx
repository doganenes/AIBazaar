import React, { useState } from "react";
import axios from "axios";

function GeneratePrice() {
  const [formData, setFormData] = useState({
    storage: "",
    ram: "",
    display_size: "",
    os: "",
    battery: "",
    foldable: "",
    display_type: "",
    video_resolution: "",
    ppi: "",
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
      alert(`Tahmin edilen fiyat: ${response.data.price} USD`);
      setPredictedPrice(response.data.price);
    } catch (error) {
      console.error("API isteği başarısız:", error);
      alert("Fiyat tahmini yapılamadı.");
      setPredictedPrice(null);
    }
  };
  return (
    <div className="container my-5">
      <div className="row justify-content-center g-4">
        <div className="col-12 col-md-5 mb-4 p-3 bg-secondary rounded ms-md-4">
          <form onSubmit={handleSubmit}>
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
                <option value="android">Android</option>
                <option value="ios">iOS</option>
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
                <option value="Super Retina">Super Retina</option>
                <option value="Amoled">Amoled</option>
                <option value="IPS">IPS LCD</option>
                <option value="Oled">OLED</option>
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
                <option value="8K">8K</option>
                <option value="4K">4K</option>
                <option value="1080P">1080P</option>
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

            <button type="submit" className="btn btn-primary">
              Submit
            </button>
            {predictedPrice !== null && (
              <div className="alert alert-info mt-4" role="alert">
                Tahmin edilen fiyat: <strong>{predictedPrice} USD</strong>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
}

export default GeneratePrice;
