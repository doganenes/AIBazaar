import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "../css/Footer.css";

function Footer() {
  return (
    <footer className="bg-dark text-white mt-5 pt-4 pb-3 w-100">
      <div className="container">
        <div className="row text-center text-md-start align-items-center">
          <div className="col-md-4 mb-3">
            <h5 className="fw-bold">AIBazaar</h5>
          </div>
          <div className="col-md-4 mb-3 mb-md-0">
            <p className="mb-0">&copy; 2025 AIBazaar</p>
          </div>
          <div className="col-md-4">
            <div className="d-flex flex-column flex-md-row justify-content-center justify-content-md-end gap-2">
              <a href="/favorites" className="text-white text-decoration-none">
                Favorites
              </a>
              <a href="/signup" className="text-white text-decoration-none">
                Signup
              </a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
