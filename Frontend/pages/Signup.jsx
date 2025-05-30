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
    <div
      className="min-vh-100"
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      }}
    >
      <div className="container-fluid h-100">
        <div className="row min-vh-100">
          <div className="col-lg-7 col-md-6 d-flex align-items-center justify-content-center text-white p-5">
            <div className="text-center">
              <div className="mb-5">
                <div className="d-flex align-items-center justify-content-center mb-4">
                  <div
                    className="rounded-3 me-3 d-flex align-items-center justify-content-center"
                    style={{
                      width: "60px",
                      height: "60px",
                      background: "rgba(255, 255, 255, 0.2)",
                      backdropFilter: "blur(10px)",
                    }}
                  >
                    <i className="fas fa-chart-line fs-2"></i>
                  </div>
                  <h1 className="fs-1 fw-bold mb-0">AIBazaar</h1>
                </div>
              </div>

              <div className="mb-5">
                <h2 className="display-5 fw-bold mb-4">
                  Transform your business with intelligent pricing
                </h2>
                <p className="fs-5 mb-4 opacity-90">
                  Harness the power of AI to predict market trends, optimize
                  pricing strategies, and maximize your revenue potential.
                </p>
              </div>

              <div className="row text-start">
                <div className="col-md-6 mb-4">
                  <div className="d-flex align-items-start">
                    <div
                      className="rounded-circle me-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                      style={{
                        width: "50px",
                        height: "50px",
                        background: "rgba(255, 255, 255, 0.2)",
                      }}
                    >
                      <i className="fas fa-brain"></i>
                    </div>
                    <div>
                      <h5 className="fw-bold mb-2">AI-Powered Analysis</h5>
                      <p className="opacity-90 mb-0">
                        Advanced machine learning algorithms analyze market data
                        in real-time
                      </p>
                    </div>
                  </div>
                </div>

                <div className="col-md-6 mb-4">
                  <div className="d-flex align-items-start">
                    <div
                      className="rounded-circle me-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                      style={{
                        width: "50px",
                        height: "50px",
                        background: "rgba(255, 255, 255, 0.2)",
                      }}
                    >
                      <i className="fas fa-chart-bar"></i>
                    </div>
                    <div>
                      <h5 className="fw-bold mb-2">Smart Predictions</h5>
                      <p className="opacity-90 mb-0">
                        Accurate price forecasting based on historical and
                        market data
                      </p>
                    </div>
                  </div>
                </div>

                <div className="col-md-6 mb-4">
                  <div className="d-flex align-items-start">
                    <div
                      className="rounded-circle me-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                      style={{
                        width: "50px",
                        height: "50px",
                        background: "rgba(255, 255, 255, 0.2)",
                      }}
                    >
                      <i className="fas fa-rocket"></i>
                    </div>
                    <div>
                      <h5 className="fw-bold mb-2">Instant Results</h5>
                      <p className="opacity-90 mb-0">
                        Get pricing recommendations in seconds, not hours
                      </p>
                    </div>
                  </div>
                </div>

                <div className="col-md-6 mb-4">
                  <div className="d-flex align-items-start">
                    <div
                      className="rounded-circle me-3 flex-shrink-0 d-flex align-items-center justify-content-center"
                      style={{
                        width: "50px",
                        height: "50px",
                        background: "rgba(255, 255, 255, 0.2)",
                      }}
                    >
                      <i className="fas fa-shield-alt"></i>
                    </div>
                    <div>
                      <h5 className="fw-bold mb-2">Secure & Reliable</h5>
                      <p className="opacity-90 mb-0">
                        Enterprise-grade security with 99.9% uptime guarantee
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div
            className="col-lg-5 col-md-6 d-flex align-items-center justify-content-center"
            style={{ background: "#f8f9ff" }}
          >
            <div className="w-100 px-4" style={{ maxWidth: "450px" }}>
              <div
                className="p-5 rounded-4 shadow-lg bg-white"
                style={{
                  border: "1px solid rgba(102, 126, 234, 0.1)",
                }}
              >
                <div className="text-center mb-4">
                  <div
                    className="d-inline-flex align-items-center justify-content-center rounded-circle mb-3"
                    style={{
                      width: "70px",
                      height: "70px",
                      background:
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                      color: "white",
                    }}
                  >
                    <i className="fas fa-user-plus fs-3"></i>
                  </div>
                  <h2
                    className="fw-bold mb-2"
                    style={{
                      background:
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                      WebkitBackgroundClip: "text",
                      WebkitTextFillColor: "transparent",
                      backgroundClip: "text",
                    }}
                  >
                    Create Account
                  </h2>
                  <p className="text-muted">
                    Join AIBazaar and start optimizing your pricing
                  </p>
                </div>

                {message && (
                  <Alert
                    variant={variant}
                    className="d-flex align-items-center py-3 mb-4 rounded-3 border-0"
                    style={{
                      background:
                        variant === "success"
                          ? "rgba(25, 135, 84, 0.1)"
                          : "rgba(220, 53, 69, 0.1)",
                      color: variant === "success" ? "#198754" : "#dc3545",
                      border: `1px solid ${
                        variant === "success"
                          ? "rgba(25, 135, 84, 0.2)"
                          : "rgba(220, 53, 69, 0.2)"
                      }`,
                    }}
                  >
                    <i
                      className={`fas ${
                        variant === "success"
                          ? "fa-check-circle"
                          : "fa-exclamation-triangle"
                      } me-2`}
                    ></i>
                    {message}
                  </Alert>
                )}

                <Form onSubmit={handleSubmit}>
                  <div className="row">
                    <div className="col-md-6">
                      <Form.Group className="mb-3" controlId="firstName">
                        <Form.Label className="fw-semibold text-dark">
                          First Name
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="firstName"
                          placeholder="John"
                          value={formData.firstName}
                          onChange={handleChange}
                          required
                          className="py-3 rounded-3"
                          style={{
                            fontSize: "1rem",
                            border: "2px solid #e9ecef",
                            transition: "all 0.3s ease",
                          }}
                        />
                      </Form.Group>
                    </div>
                    <div className="col-md-6">
                      <Form.Group className="mb-3" controlId="lastName">
                        <Form.Label className="fw-semibold text-dark">
                          Last Name
                        </Form.Label>
                        <Form.Control
                          type="text"
                          name="lastName"
                          placeholder="Doe"
                          value={formData.lastName}
                          onChange={handleChange}
                          required
                          className="py-3 rounded-3"
                          style={{
                            fontSize: "1rem",
                            border: "2px solid #e9ecef",
                            transition: "all 0.3s ease",
                          }}
                        />
                      </Form.Group>
                    </div>
                  </div>

                  <Form.Group className="mb-3" controlId="email">
                    <Form.Label className="fw-semibold text-dark">
                      Email Address
                    </Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      placeholder="john.doe@example.com"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="py-3 rounded-3"
                      style={{
                        fontSize: "1rem",
                        border: "2px solid #e9ecef",
                        transition: "all 0.3s ease",
                      }}
                    />
                  </Form.Group>

                  <Form.Group className="mb-3" controlId="password">
                    <Form.Label className="fw-semibold text-dark">
                      Password
                    </Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      placeholder="Enter secure password"
                      value={formData.password}
                      onChange={handleChange}
                      required
                      className="py-3 rounded-3"
                      style={{
                        fontSize: "1rem",
                        border: "2px solid #e9ecef",
                        transition: "all 0.3s ease",
                      }}
                    />
                  </Form.Group>

                  <Form.Group className="mb-4" controlId="confirmPassword">
                    <Form.Label className="fw-semibold text-dark">
                      Confirm Password
                    </Form.Label>
                    <Form.Control
                      type="password"
                      name="confirmPassword"
                      placeholder="Confirm your password"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                      required
                      className="py-3 rounded-3"
                      style={{
                        fontSize: "1rem",
                        border: "2px solid #e9ecef",
                        transition: "all 0.3s ease",
                      }}
                    />
                  </Form.Group>

                  <Button
                    type="submit"
                    className="w-100 py-3 rounded-3 border-0 fw-semibold fs-5 mb-4"
                    style={{
                      background:
                        "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                      transition: "all 0.3s ease",
                      boxShadow: "0 4px 15px rgba(102, 126, 234, 0.3)",
                    }}
                  >
                    <i className="fas fa-user-plus me-2"></i>
                    Create Account
                  </Button>
                </Form>

                <div className="text-center border-top pt-4">
                  <p className="text-muted mb-0">
                    Already have an account?{" "}
                    <a
                      href="/signin"
                      className="text-decoration-none fw-semibold"
                      style={{
                        background:
                          "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        WebkitBackgroundClip: "text",
                        WebkitTextFillColor: "transparent",
                        backgroundClip: "text",
                      }}
                    >
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
