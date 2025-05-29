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
      className="min-vh-100 d-flex align-items-center mt-5 justify-content-center py-5"
      style={{
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        className="position-absolute"
        style={{
          width: "250px",
          height: "250px",
          background: "rgba(255,255,255,0.1)",
          borderRadius: "50%",
          top: "10%",
          left: "5%",
          animation: "float 7s ease-in-out infinite",
        }}
      />
      <div
        className="position-absolute"
        style={{
          width: "180px",
          height: "180px",
          background: "rgba(255,255,255,0.08)",
          borderRadius: "50%",
          bottom: "5%",
          right: "8%",
          animation: "float 5s ease-in-out infinite reverse",
        }}
      />
      <div
        className="position-absolute"
        style={{
          width: "120px",
          height: "120px",
          background: "rgba(255,255,255,0.06)",
          borderRadius: "50%",
          top: "70%",
          left: "85%",
          animation: "float 9s ease-in-out infinite",
        }}
      />

      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-5 col-md-7 col-sm-9 col-12">
            <div
              className="p-5 rounded-4 shadow-lg"
              style={{
                background: "rgba(255, 255, 255, 0.95)",
                backdropFilter: "blur(20px)",
                border: "1px solid rgba(255, 255, 255, 0.2)",
                maxWidth: "500px",
                margin: "0 auto",
              }}
            >
              <div className="text-center mb-4">
                <div
                  className="d-inline-flex align-items-center justify-content-center rounded-circle mb-3"
                  style={{
                    width: "80px",
                    height: "80px",
                    background:
                      "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    color: "white",
                  }}
                >
                  <i className="fas fa-user-plus fs-2"></i>
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
                  Signup
                </h2>
                <p className="text-muted">Create new account</p>
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
                        <i className="fas fa-user me-2 text-muted"></i>
                        First Name
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="firstName"
                        placeholder="Enter your name"
                        value={formData.firstName}
                        onChange={handleChange}
                        required
                        className="py-3 rounded-3 border-2"
                        style={{
                          fontSize: "1rem",
                          transition: "all 0.3s ease",
                          borderColor: "#e0e0e0",
                        }}
                      />
                    </Form.Group>
                  </div>
                  <div className="col-md-6">
                    <Form.Group className="mb-3" controlId="lastName">
                      <Form.Label className="fw-semibold text-dark">
                        <i className="fas fa-user me-2 text-muted"></i>
                        Last Name
                      </Form.Label>
                      <Form.Control
                        type="text"
                        name="lastName"
                        placeholder="Enter your surname"
                        value={formData.lastName}
                        onChange={handleChange}
                        required
                        className="py-3 rounded-3 border-2"
                        style={{
                          fontSize: "1rem",
                          transition: "all 0.3s ease",
                          borderColor: "#e0e0e0",
                        }}
                      />
                    </Form.Group>
                  </div>
                </div>

                <Form.Group className="mb-3" controlId="email">
                  <Form.Label className="fw-semibold text-dark">
                    <i className="fas fa-envelope me-2 text-muted"></i>
                    Email
                  </Form.Label>
                  <Form.Control
                    type="email"
                    name="email"
                    placeholder="Enter your email"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    className="py-3 rounded-3 border-2"
                    style={{
                      fontSize: "1rem",
                      transition: "all 0.3s ease",
                      borderColor: "#e0e0e0",
                    }}
                  />
                </Form.Group>

                <Form.Group className="mb-3" controlId="password">
                  <Form.Label className="fw-semibold text-dark">
                    <i className="fas fa-lock me-2 text-muted"></i>
                    Password
                  </Form.Label>
                  <Form.Control
                    type="password"
                    name="password"
                    placeholder="Enter your password"
                    value={formData.password}
                    onChange={handleChange}
                    required
                    className="py-3 rounded-3 border-2"
                    style={{
                      fontSize: "1rem",
                      transition: "all 0.3s ease",
                      borderColor: "#e0e0e0",
                    }}
                  />
                </Form.Group>

                <Form.Group className="mb-4" controlId="confirmPassword">
                  <Form.Label className="fw-semibold text-dark">
                    <i className="fas fa-check-circle me-2 text-muted"></i>
                    Confirm Password
                  </Form.Label>
                  <Form.Control
                    type="password"
                    name="confirmPassword"
                    placeholder="Confirm your password"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    required
                    className="py-3 rounded-3 border-2"
                    style={{
                      fontSize: "1rem",
                      transition: "all 0.3s ease",
                      borderColor: "#e0e0e0",
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
                    transform: "translateY(0)",
                    boxShadow: "0 4px 15px rgba(102, 126, 234, 0.3)",
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = "translateY(-2px)";
                    e.target.style.boxShadow =
                      "0 8px 25px rgba(102, 126, 234, 0.4)";
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = "translateY(0)";
                    e.target.style.boxShadow =
                      "0 4px 15px rgba(102, 126, 234, 0.3)";
                  }}
                >
                  <i className="fas fa-user-plus me-2"></i>
                  Signup
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
                    Signin
                  </a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
