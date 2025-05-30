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
    <div
      className="min-vh-100 d-flex"
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      }}
    >
      <div className="container-fluid h-100">
        <div className="row min-vh-100 align-items-stretch">
          <div className="col-lg-6 col-md-6 d-flex flex-column justify-content-center p-5 text-white">
            {/* Logo */}
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
                <h1 className="fs-1 fw-bold mb-0 ">AIBazaar</h1>
              </div>
            </div>

            <div className="mb-5">
              <h2 className="display-4 fw-bold mb-4">
                Welcome back to intelligent pricing
              </h2>
              <p className="fs-4 mb-4 opacity-90">
                Continue optimizing your business with AI-powered market
                analysis and smart pricing strategies.
              </p>
            </div>
          </div>

          <div className="col-lg-6 col-md-6 d-flex align-items-center justify-content-center bg-white">
            <div className="w-100 px-4" style={{ maxWidth: "450px" }}>
              <div
                className="p-5 rounded-4 shadow-lg bg-white"
                style={{
                  border: "1px solid rgba(102, 126, 234, 0.1)",
                }}
              >
                <div className="text-center mb-4">
                  <h2 className="fw-bold mb-2">Sign In</h2>
                  <p className="text-muted">
                    Enter your credentials to access your account
                  </p>
                </div>

                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3" controlId="formEmail">
                    <Form.Label className="fw-semibold text-dark">
                      Email Address
                    </Form.Label>
                    <Form.Control
                      type="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      placeholder="Enter your email"
                      isInvalid={!!errors.email}
                      className="py-3 rounded-3"
                      style={{
                        fontSize: "1rem",
                        border: errors.email
                          ? "2px solid #dc3545"
                          : "2px solid #e9ecef",
                        transition: "all 0.3s ease",
                      }}
                    />
                    {errors.email && (
                      <Form.Control.Feedback
                        type="invalid"
                        className="fw-medium"
                      >
                        <i className="fas fa-exclamation-circle me-1"></i>
                        {errors.email}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>

                  <Form.Group className="mb-4" controlId="formPassword">
                    <Form.Label className="fw-semibold text-dark">
                      Password
                    </Form.Label>
                    <Form.Control
                      type="password"
                      name="password"
                      value={formData.password}
                      onChange={handleChange}
                      placeholder="Enter your password"
                      isInvalid={!!errors.password}
                      className="py-3 rounded-3"
                      style={{
                        fontSize: "1rem",
                        border: errors.password
                          ? "2px solid #dc3545"
                          : "2px solid #e9ecef",
                        transition: "all 0.3s ease",
                      }}
                    />
                    {errors.password && (
                      <Form.Control.Feedback
                        type="invalid"
                        className="fw-medium"
                      >
                        <i className="fas fa-exclamation-circle me-1"></i>
                        {errors.password}
                      </Form.Control.Feedback>
                    )}
                  </Form.Group>

                  {errorMessage && (
                    <div
                      className="alert alert-danger d-flex align-items-center py-3 mb-3 rounded-3 border-0"
                      role="alert"
                      style={{
                        background: "rgba(220, 53, 69, 0.1)",
                        color: "#dc3545",
                        border: "1px solid rgba(220, 53, 69, 0.2)",
                      }}
                    >
                      <i className="fas fa-exclamation-triangle me-2"></i>
                      {errorMessage}
                    </div>
                  )}

                  {successMessage && (
                    <div
                      className="alert alert-success d-flex align-items-center py-3 mb-3 rounded-3 border-0"
                      role="alert"
                      style={{
                        background: "rgba(25, 135, 84, 0.1)",
                        color: "#198754",
                        border: "1px solid rgba(25, 135, 84, 0.2)",
                      }}
                    >
                      <i className="fas fa-check-circle me-2"></i>
                      {successMessage}
                    </div>
                  )}

                  <Button
                    type="submit"
                    disabled={isLoading}
                    className="w-100 py-3 rounded-3 border-0 fw-semibold fs-5 mb-4"
                    style={{
                      background: isLoading
                        ? "linear-gradient(135deg, #cccccc 0%, #999999 100%)"
                        : "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                      transition: "all 0.3s ease",
                      transform: "translateY(0)",
                      boxShadow: "0 4px 15px rgba(102, 126, 234, 0.3)",
                    }}
                  >
                    {isLoading ? (
                      <>
                        <i className="fas fa-spinner fa-spin me-2"></i>
                        Signing in...
                      </>
                    ) : (
                      <>
                        <i className="fas fa-sign-in-alt me-2"></i>
                        Sign In
                      </>
                    )}
                  </Button>
                </Form>

                <div className="text-center border-top pt-4">
                  <p className="text-muted mb-0">
                    Don't have an account?{" "}
                    <a
                      href="/signup"
                      className="text-decoration-none fw-semibold"
                      style={{
                        background:
                          "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                        WebkitBackgroundClip: "text",
                        WebkitTextFillColor: "transparent",
                        backgroundClip: "text",
                      }}
                    >
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
