import React from 'react';
import { Form, Button } from 'react-bootstrap';
import "../css/Signin.css";

const Signin = () => {
  return (
    <div className="container d-flex justify-content-center mt-5 min-vh-100">
      <div className="signin-form bg-light p-4 rounded shadow-sm w-100" style={{ maxWidth: '400px', maxHeight:"400px"}}>
        <h2 className="mb-4 text-center">Signin</h2>

        <Form>
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

          <Button className="btn mt-3 btn-dark w-100" type="submit">
            Login
          </Button>
        </Form>

        <div className="mt-5 text-center">
          <span>Don't have an account? </span>
          <a href="/signup" className="text-decoration-none">
            Sign Up
          </a>
        </div>
      </div>
    </div>
  );
};

export default Signin;
