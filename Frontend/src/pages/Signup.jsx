import React, { useState } from "react";
import { Form, Button, Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import "../css/Signup.css";
import { register } from "../api/api";

const Signup = () => {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [message, setMessage] = useState(null);
  const [variant, setVariant] = useState("danger");

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setMessage("Passwords do not match.");
      setVariant("danger");
      return;
    }

    const { confirmPassword, ...requestData } = formData;

    try {
      const result = await register(requestData);

      if (result.success === false) {
        setMessage(result.message || "Registration failed.");
        setVariant("danger");
      } else {
        setMessage("Registration successful!");
        setVariant("success");
        setTimeout(() => {
          navigate("/home");
        }, 1000);
      }
    } catch (err) {
      setMessage("An unexpected error occurred.");
      setVariant("danger");
    }
  };

  return (
    <div className="signup-container">
      <div className="container-fluid h-100">
        <div className="row signup-row">
          {/* Sol Panel - Bilgi ve Özellikler */}
          <div className="col-lg-7 col-md-6 info-panel">
            <div className="info-content">
              <div className="brand-container">
                <div className="brand-header">
                  <div className="brand-icon">
                    <i className="fas fa-chart-bar fs-2"></i>
                  </div>
                  <h1 className="brand-title">AIBazaar</h1>
                </div>
              </div>

              <div className="hero-section">
                <h2 className="hero-title">
                  Transform your business with intelligent pricing
                </h2>
                <p className="hero-description">
                  Harness the power of AI to predict market trends, optimize
                  pricing strategies, and maximize your revenue potential.
                </p>
              </div>

              <div className="features-grid">
                <div className="row">
                  <div className="col-md-6 feature-item">
                    <div className="feature-content">
                      <div className="feature-icon">
                        <i className="fas fa-brain"></i>
                      </div>
                      <div>
                        <h5 className="feature-title">AI-Powered Analysis</h5>
                        <p className="feature-description">
                          Advanced machine learning algorithms analyze market
                          data in real-time
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-6 feature-item">
                    <div className="feature-content">
                      <div className="feature-icon">
                        <i className="fas fa-chart-bar"></i>
                      </div>
                      <div>
                        <h5 className="feature-title">Smart Predictions</h5>
                        <p className="feature-description">
                          Accurate price forecasting based on historical and
                          market data
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-6 feature-item">
                    <div className="feature-content">
                      <div className="feature-icon">
                        <i className="fas fa-rocket"></i>
                      </div>
                      <div>
                        <h5 className="feature-title">Instant Results</h5>
                        <p className="feature-description">
                          Get pricing recommendations in seconds, not hours
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="col-md-6 feature-item">
                    <div className="feature-content">
                      <div className="feature-icon">
                        <i className="fas fa-shield-alt"></i>
                      </div>
                      <div>
                        <h5 className="feature-title">Secure & Reliable</h5>
                        <p className="feature-description">
                          Enterprise-grade security with 99.9% uptime guarantee
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Sağ Panel - Form */}
          <div className="col-lg-5 col-md-6 form-panel">
            <div className="form-wrapper">
              <div className="form-card">
                <div className="form-header">
                  <div className="form-icon">
                    <i className="fas fa-user-plus fs-3"></i>
                  </div>
                  <h2 className="form-title">Create Account</h2>
                  <p className="form-subtitle">
                    Join AIBazaar and start optimizing your pricing
                  </p>
                </div>

                {message && (
                  <Alert
                    variant={variant}
                    className={`custom-alert ${
                      variant === "success" ? "alert-success" : "alert-danger"
                    }`}
                  >
                    <i
                      className={`fas ${
                        variant === "success"
                          ? "fa-check-circle"
                          : "fa-exclamation-triangle"
                      } alert-icon`}
                    ></i>
                    {message}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <div className="row">
                    <div className="col-md-6">
                      <Form.Group className="mb-3" controlId="firstName">
                        <Form.Label className="form-label">
                          First Name
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="firstName"
                          placeholder="John"
                          value={formData.firstName}
                          onChange={handleChange}
                          required
                          className="form-input"
                        />
                      </Form.Group>
                    </div>
                    <div className="col-md-6">
                      <Form.Group className="mb-3" controlId="lastName">
                        <Form.Label className="form-label">
                          Last Name
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="lastName"
                          placeholder="Doe"
                          value={formData.lastName}
                          onChange={handleChange}
                          required
                          className="form-input"
                        />
                      </Form.Group>
                    </div>
                  </div>

                  <Form.Group className="mb-3" controlId="email">
                    <Form.Label className="form-label">
                      Email Address
                    </Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      placeholder="john.doe@example.com"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="form-input"
                    />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="password">
                    <Form.Label className="form-label">Password</Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      placeholder="Enter secure password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      className="form-input"
                    />
                  </Form.Group>

                  <Form.Group className="mb-4" controlId="confirmPassword">
                    <Form.Label className="form-label">
                      Confirm Password
                    </Form.Label>
                    <Form.Control
                      type="password"
                      name="confirmPassword"
                      placeholder="Confirm your password"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      required
                      className="form-input"
                    />
                  </Form.Group>

                  <Button type="submit" className="submit-button">
                    <i className="fas fa-user-plus me-2"></i>
                    Create Account
                  </Button>
                </Form>

                <div className="form-footer">
                  <p className="footer-text">
                    Already have an account?{" "}
                    <a href="/signin" className="footer-link">
                      Sign In
                    </a>
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
