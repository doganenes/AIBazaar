import { Form, Button } from "react-bootstrap";
import "../css/Signin.css";
import { login, tokenToId } from "../api/api";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const Signin = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState("");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    console.log(`Token değeri: ${token}`);

    if (token) {
      navigate("/home");
    }
  }, [navigate]);

  const validate = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = "Email is required!";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid!";
    }
    if (!formData.password) {
      newErrors.password = "Password is required!";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters!";
    }
    return newErrors;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
    setErrorMessage("");

    if (errors[name]) {
      setErrors({
        ...errors,
        [name]: null,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const validationErrors = validate();

    console.log("Form verileri gönderilmeye hazırlanıyor:", formData);

    if (Object.keys(validationErrors).length === 0) {
      setErrors({});
      setIsLoading(true);

      try {
        console.log("API'ye gönderilen veriler:", formData);
        const response = await login(formData);
        console.log("API'den dönen yanıt:", response);

        if (response && response.message === "Login successful.") {
          setSuccess(true);
          localStorage.setItem("authToken", response.token);
          console.log(`Dönen tokenimiz : ${response.token}`);
          setSuccessMessage("Login successful!");
          navigate("/home");

          try {
          } catch (idError) {
            console.error("Token to ID error:", idError);
          }
        } else {
          const errorMsg = response?.message || "Incorrect email or password";
          setErrorMessage(errorMsg);
          setSuccess(false);
        }
      } catch (error) {
        console.error("Login hatası:", error);
        setErrorMessage("An error occurred while signing in.");
        setSuccess(false);
      } finally {
        setIsLoading(false);
      }
    } else {
      setErrors(validationErrors);
      setSuccess(false);
    }
  };

  useEffect(() => {
    if (isLoggedIn) {
      navigate("/home");
    }
  }, [isLoggedIn, navigate]);

  return (
    <div className="signin-container">
      <div className="container-fluid h-100">
        <div className="row signin-row">
          {/* Sol Panel - Welcome */}
          <div className="col-lg-6 col-md-6 welcome-panel">
            {/* Logo */}
            <div className="brand-section">
              <div className="brand-header">
                <div className="brand-icon">
                  <i className="fas fa-chart-bar fs-2"></i>
                </div>
                <h1 className="brand-title">AIBazaar</h1>
              </div>
            </div>

            <div className="welcome-content">
              <h2 className="welcome-title">
                Welcome back to intelligent pricing
              </h2>
              <p className="welcome-description">
                Continue optimizing your business with AI-powered market
                analysis and smart pricing strategies.
              </p>
            </div>
          </div>

          {/* Sağ Panel - Form */}
          <div className="col-lg-6 col-md-6 form-panel">
            <div className="form-wrapper">
              <div className="form-card">
                <div className="form-header">
                  <h2 className="form-title">Sign In</h2>
                  <p className="form-subtitle">
                    Enter your credentials to access your account
                  </p>
                </div>

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3" controlId="formEmail">
                    <Form.Label className="form-label">
                      Email Address
                    </Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="Enter your email"
                      isInvalid={!!errors.email}
                      className={`form-input ${
                        errors.email ? "form-input-error" : "form-input-default"
                      }`}
                    />
                    {errors.email && (
                      <Form.Control.Feedback
                        type="invalid"
                        className="error-feedback"
                      >
                        <i className="fas fa-exclamation-circle error-icon"></i>
                        {errors.email}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>

                  <Form.Group className="mb-4" controlId="formPassword">
                    <Form.Label className="form-label">Password</Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter your password"
                      isInvalid={!!errors.password}
                      className={`form-input ${
                        errors.password
                          ? "form-input-error"
                          : "form-input-default"
                      }`}
                    />
                    {errors.password && (
                      <Form.Control.Feedback
                        type="invalid"
                        className="error-feedback"
                      >
                        <i className="fas fa-exclamation-circle error-icon"></i>
                        {errors.password}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>

                  {errorMessage && (
                    <div className="custom-alert alert-danger" role="alert">
                      <i className="fas fa-exclamation-triangle alert-icon"></i>
                      {errorMessage}
                    </div>
                  )}

                  {successMessage && (
                    <div className="custom-alert alert-success" role="alert">
                      <i className="fas fa-check-circle alert-icon"></i>
                      {successMessage}
                    </div>
                  )}

                  <Button
                    type="submit"
                    disabled={isLoading}
                    className={`submit-button ${
                      isLoading
                        ? "submit-button-loading"
                        : "submit-button-normal"
                    }`}
                  >
                    {isLoading ? (
                      <>
                        <i className="fas fa-spinner fa-spin loading-spinner"></i>
                        Signing in...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-sign-in-alt submit-icon"></i>
                        Sign In
                      </>
                    )}
                  </Button>
                </Form>

                <div className="form-footer">
                  <p className="footer-text">
                    Don't have an account?{" "}
                    <a href="/signup" className="footer-link">
                      Sign Up
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

export default Signin;
