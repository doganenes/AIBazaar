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
        [name]: null
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
          console.log(`Dönen tokenimiz : ${response.token}`)
          setSuccessMessage("Login successful!");
          navigate("/home")
          
          
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
        setErrorMessage("Sunucu bağlantısında hata oluştu. Lütfen tekrar deneyin.");
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
    <div className="container d-flex justify-content-center mt-5 min-vh-100">
      <div
        className="signin-form bg-light p-4 rounded shadow-sm w-100"
        style={{ maxWidth: "400px", maxHeight: "450px" }}
      >
        <h2 className="mb-4 text-center">Giriş Yap</h2>

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-2" controlId="formEmail">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="Email adresinizi girin"
              isInvalid={!!errors.email}
            />
            {errors.email && (
              <Form.Control.Feedback type="invalid">
                {errors.email}
              </Form.Control.Feedback>
            )}
          </Form.Group>

          <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Şifre</Form.Label>
            <Form.Control
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Şifrenizi girin"
              isInvalid={!!errors.password}
            />
            {errors.password && (
              <Form.Control.Feedback type="invalid">
                {errors.password}
              </Form.Control.Feedback>
            )}
          </Form.Group>

          {errorMessage && (
            <div className="alert alert-danger py-2 mb-3" role="alert">
              {errorMessage}
            </div>
          )}

          {successMessage && (
            <div className="alert alert-success py-2 mb-3" role="alert">
              {successMessage}
            </div>
          )}

          <Button 
            className="btn mt-2 btn-dark w-100" 
            type="submit"
            disabled={isLoading}
          >
            {isLoading ? 'Giriş yapılıyor...' : 'Giriş Yap'}
          </Button>
        </Form>

        <div className="mt-4 text-center">
          <span>Hesabınız yok mu? </span>
          <a href="/signup" className="text-decoration-none">
            Kayıt Ol
          </a>
        </div>
      </div>
    </div>
  );
};

export default Signin;