import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import "../css/Signup.css";
import { register } from '../api/api'; 
const Signup = () => {
  const navigate = useNavigate(); 

  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: ''
  });

  const [message, setMessage] = useState(null);
  const [variant, setVariant] = useState('danger');

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setMessage('Passwords do not match.');
      setVariant('danger');
      return;
    }

    const { confirmPassword, ...requestData } = formData;

    try {
      const result = await register(requestData);

      if (result.success === false) {
        setMessage(result.message || 'Registration failed.');
        setVariant('danger');
      } else {
        setMessage('Registration successful!');
        setVariant('success');
        setTimeout(() => {
          navigate('/home');
        }, 1000);
      }
    } catch (err) {
      setMessage('An unexpected error occurred.');
      setVariant('danger');
    }
  };

  return (
    <div className="container d-flex justify-content-center min-vh-100">
      <div className="signin-form bg-light p-4 rounded shadow-sm w-100" style={{ maxWidth: '400px', maxHeight: "650px" }}>
        <h2 className="mb-4 text-center">Signup</h2>

        {message && <Alert variant={variant}>{message}</Alert>}

        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-2" controlId="firstName">
            <Form.Label>First Name</Form.Label>
            <Form.Control
              type="text"
              name="firstName"
              placeholder="Enter your name"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-2" controlId="lastName">
            <Form.Label>Last Name</Form.Label>
            <Form.Control
              type="text"
              name="lastName"
              placeholder="Enter your surname"
              value={formData.lastName}
              onChange={handleChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-2" controlId="email">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              name="email"
              placeholder="Enter your email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="password">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              name="password"
              placeholder="Enter your password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="confirmPassword">
            <Form.Label>Confirm Password</Form.Label>
            <Form.Control
              type="password"
              name="confirmPassword"
              placeholder="Confirm your password"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </Form.Group>

          <Button className="btn mt-3 btn-info w-100" type="submit">
            Signup
          </Button>
        </Form>

        <div className="mt-5 text-center">
          <span>Already have an account? </span>
          <a href="/signin" className="text-decoration-none">
            Signin
          </a>
        </div>
      </div>
    </div>
  );
};

export default Signup;
