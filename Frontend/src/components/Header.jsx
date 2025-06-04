import React, { useState, useEffect } from "react";
import { getAllFavoriteProducts, tokenToId, logout,getUserFromId, addFavoriteProduct } from "../api/api";
import { useNavigate } from "react-router-dom";
import "../css/Header.css";

function Header() {
  const [searchTerm, setSearchTerm] = useState("");
  const [user, setUser] = useState(null);
  const [favoriteProducts, setFavoriteProducts] = useState(null);
  const [isLoadingFavorites, setIsLoadingFavorites] = useState(true);
  const navigate = useNavigate();
  const handleSearch = () => {
    console.log("Searching for:", searchTerm);
  };

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const userId = await tokenToId();
        console.log("User ID from token:", userId);
        const favorites = await addFavoriteProduct(userId);
        const userData = await getUserFromId(userId);
        setUser(userData);
        setFavoriteProducts(favorites);
      } catch (error) {
        console.error("Favorites not found:", error.message || error);
      } finally {
        setIsLoadingFavorites(false);
      }
    };
    fetchFavorites();
  }, []);

  const handleLogout = async (e) => {
    e.preventDefault();
    await logout();
    navigate("/signin");
  };

  return (
    <nav
      className="navbar navbar-expand-lg fixed-top shadow-lg py-3"
      style={{
        background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      }}
    >
      <div className="container">
        <a
          className="navbar-brand d-flex align-items-center text-white"
          href="/"
        >
          <i className="fas fa-chart-bar me-2 fs-4"></i>
          <span className="fs-3 fw-bold">AIBazaar</span>
        </a>

        <button
          className="navbar-toggler border-0"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarContent"
          style={{ boxShadow: "none" }}
        >
          <i className="fas fa-bars text-white"></i>
        </button>

        <div className="collapse navbar-collapse" id="navbarContent">
          <div
            className="d-flex mx-auto my-3 my-lg-0"
            style={{ width: "100%", maxWidth: "500px" }}
          >
            <div className="input-group">
              <input
                className="form-control border-0 shadow-sm"
                type="search"
                placeholder="Search Product.."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  borderRadius: "25px 0 0 25px",
                  fontSize: "0.95rem",
                }}
              />
              <button
                className="btn btn-light border-0 shadow-sm px-4"
                onClick={handleSearch}
                style={{
                  borderRadius: "0 25px 25px 0",
                  background: "white",
                }}
              >
                <i className="fas fa-search text-primary"></i>
              </button>
            </div>
          </div>

          <div className="d-flex flex-column flex-lg-row align-items-center ms-lg-3">
            <a
              href="/generateprice"
              className="nav-link text-white d-flex align-items-center me-lg-3 mb-2 mb-lg-0 nav-item-hover"
            >
              <i class="fas fa-chart-line me-1"></i>
              <span>Forecast</span>
            </a>

            <a
              href="/favorites"
              className="nav-link text-white d-flex align-items-center me-lg-3 mb-2 mb-lg-0 nav-item-hover"
            >
              <i className="fas fa-heart me-1"></i>
              <span>Favorites</span>
              <span className="badge bg-danger ms-1 rounded-pill">
                {!isLoadingFavorites && favoriteProducts !== null
                  ? favoriteProducts.length
                  : ""}
              </span>
            </a>

            <div className="dropdown">
              <button
                className="btn btn-outline-light dropdown-toggle border-2 px-3"
                type="button"
                data-bs-toggle="dropdown"
                style={{ borderRadius: "25px" }}
              >
                <i className="fas fa-user me-1"></i>
                {user ? `${user.firstName} ${user.lastName}` : "Loading..."}
              </button>
              <ul
                className="dropdown-menu dropdown-menu-end shadow-lg border-0 mt-2"
                style={{ borderRadius: "15px" }}
              >
                <li>
                  <a
                    className="dropdown-item py-2 text-danger"
                    onClick={handleLogout}
                    href="/logout"
                  >
                    <i className="fas fa-sign-out-alt me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Header;