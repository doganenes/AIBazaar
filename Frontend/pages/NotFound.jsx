import React from "react";
import { Link } from "react-router-dom";
import "../css/NotFound.css";

function NotFound() {
  return (
    <div
      className="min-vh-100 d-flex align-items-center mt-3 justify-content-center"
      style={{
        position: "relative",
        overflow: "hidden",
      }}
    >
      <div
        className="position-absolute"
        style={{
          width: "200px",
          height: "200px",
          background: "rgba(255,255,255,0.1)",
          borderRadius: "50%",
          top: "10%",
          left: "10%",
          animation: "float 6s ease-in-out infinite",
        }}
      ></div>
      <div
        className="position-absolute"
        style={{
          width: "150px",
          height: "150px",
          background: "rgba(255,255,255,0.05)",
          borderRadius: "50%",
          bottom: "10%",
          right: "10%",
          animation: "float 8s ease-in-out infinite reverse",
        }}
      ></div>
      <div
        className="position-absolute"
        style={{
          width: "100px",
          height: "100px",
          background: "rgba(255,255,255,0.08)",
          borderRadius: "50%",
          top: "60%",
          left: "80%",
          animation: "float 4s ease-in-out infinite",
        }}
      ></div>

      <div className="container">
        <div className="row justify-content-center">
          <div className="col-lg-6 col-md-8 col-12">
            <div
              className="text-center p-5 rounded-4 shadow-lg"
              style={{
                background: "rgba(255, 255, 255, 0.95)",
                backdropFilter: "blur(20px)",
                border: "1px solid rgba(255, 255, 255, 0.2)",
              }}
            >
              <div className="mb-4">
                <i
                  className="fas fa-exclamation-triangle"
                  style={{
                    fontSize: "4rem",
                    color: "#667eea",
                    animation: "bounce 2s infinite",
                  }}
                ></i>
              </div>

              <h1
                className="display-1 fw-bold mb-3"
                style={{
                  background:
                    "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                  fontSize: "8rem",
                  lineHeight: "1",
                }}
              >
                404
              </h1>

              <h2 className="h3 fw-bold text-dark mb-3">
                Oops! Page Not Found
              </h2>

              <p className="text-muted mb-4 fs-5">
                The page you're looking for seems to have wandered off. Don't
                worry, even the best explorers sometimes take a wrong turn!
              </p>

              <div className="d-flex flex-column flex-sm-row gap-3 justify-content-center">
                <Link
                  to="/"
                  className="btn btn-lg px-4 py-2 rounded-pill shadow-sm"
                  style={{
                    background:
                      "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                    border: "none",
                    color: "white",
                    transition: "all 0.3s ease",
                    textDecoration: "none",
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = "translateY(-2px)";
                    e.target.style.boxShadow =
                      "0 8px 25px rgba(102, 126, 234, 0.4)";
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = "translateY(0)";
                    e.target.style.boxShadow = "0 4px 15px rgba(0,0,0,0.1)";
                  }}
                >
                  <i className="fas fa-home me-2"></i>
                  Go to Homepage
                </Link>

                <button
                  onClick={() => window.history.back()}
                  className="btn btn-outline-secondary btn-lg px-4 py-2 rounded-pill"
                  style={{
                    transition: "all 0.3s ease",
                  }}
                  onMouseEnter={(e) => {
                    e.target.style.transform = "translateY(-2px)";
                    e.target.style.boxShadow = "0 8px 25px rgba(0,0,0,0.1)";
                  }}
                  onMouseLeave={(e) => {
                    e.target.style.transform = "translateY(0)";
                    e.target.style.boxShadow = "none";
                  }}
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
