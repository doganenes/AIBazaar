import React from 'react';
import { Form, Button } from 'react-bootstrap';
import "../css/Signin.css";

const Signin = () => {
  return (
    <div className="container d-flex justify-content-center min-vh-100">
      <div className="signin-form bg-light p-4 rounded shadow-sm w-100" style={{ maxWidth: '400px', maxHeight:"650px"}}>
        <h2 className="mb-4 text-center">Signup</h2>

        <Form>
          <Form.Group className="mb-2" controlId="formEmail">
            <Form.Label>First Name</Form.Label>
            <Form.Control
              type="text"
              name="firstName"
              placeholder="Enter your name"
            />
          </Form.Group>
          <Form.Group className="mb-2" controlId="formEmail">
            <Form.Label>Last Name</Form.Label>
            <Form.Control
              type="text"
              name="lastName"
              placeholder="Enter your surname"
            />
          </Form.Group>
          <Form.Group className="mb-2" controlId="formEmail">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              name="email"
              placeholder="Enter your email"
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              name="password"
              placeholder="Enter your password"
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Confirm Password</Form.Label>
            <Form.Control
              type="password"
              name="confirmPassword"
              placeholder="Confirm your password"
            />
          </Form.Group>

          <Button className="btn mt-3 btn-info w-100" type="submit">
            Signup
          </Button>
        </Form>

        <div className="mt-5 text-center">
          <span>Have already an account? </span>
          <a href="/signin" className="text-decoration-none">
            Signin
          </a>
        </div>
      </div>
    </div>
  );
};

export default Signin;
