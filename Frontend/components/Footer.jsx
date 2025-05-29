import "../css/Footer.css";

function Footer() {
  return (
    <footer className="bg-dark text-white mt-5 pt-4 pb-4 w-100 border-top border-secondary">
      <div className="container">
        <div className="row">
          <div className="col-md-4 d-flex flex-column justify-content-center text-md-start text-center mb-3 mb-md-0">
            <h5 className="fw-bold text-info mt-3">AIBazaar</h5>
            <small className="text-light">
              AI Based Price Prediction Tools
            </small>
          </div>

          <div className="col-md-4 d-flex align-items-center justify-content-center mb-3 mb-md-0">
            <small className="text-light">
              &copy; 2025 AIBazaar. All rights reserved.
            </small>
          </div>

          <div className="col-md-4 d-flex justify-content-center justify-content-md-end align-items-center gap-3">
            <a
              href="/generateprice"
              className="text-white text-decoration-none hover-link d-flex align-items-center gap-1"
            >
              <i className="bi bi-heart"></i>
              <span>Forecast</span>
            </a>

            <a
              href="/favorites"
              className="text-white text-decoration-none hover-link d-flex align-items-center gap-1"
            >
              <i className="bi bi-heart"></i>
              <span>Favorites</span>
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
