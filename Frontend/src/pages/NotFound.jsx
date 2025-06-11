import React from "react";
import { Link } from "react-router-dom";
import "../css/NotFound.css";

function NotFound() {
  return (
    <div className="notfound-wrapper">
      <div className="circle one"></div>
      <div className="circle two"></div>
      <div className="circle three"></div>

      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-6 col-md-8 col-12">
            <div className="text-center p-5 rounded-4 shadow-lg notfound-card">
              <div className="mb-4">
                <i className="fas fa-exclamation-triangle warning-icon"></i>
              </div>

              <h1 className="display-1 fw-bold mb-3 gradient-text">404</h1>

              <h2 className="h3 fw-bold text-dark mb-3">
                Oops! Page Not Found
              </h2>

              <p className="text-muted mb-4 fs-5">
                The page you're looking for seems to have wandered off. Don't
                worry, even the best explorers sometimes take a wrong turn!
              </p>

              <div className="d-flex flex-column flex-sm-row gap-3 justify-content-center">
                <Link to="/" className="btn btn-lg px-4 py-2 rounded-pill shadow-sm btn-gradient">
                  <i className="fas fa-home me-2"></i>
                  Go to Homepage
                </Link>

                <button
                  onClick={() => window.history.back()}
                  className="btn btn-outline-secondary btn-lg px-4 py-2 rounded-pill"
                >
                  <i className="fas fa-arrow-left me-2"></i>
                  Go Back
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NotFound;
