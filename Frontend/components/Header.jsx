import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import "../css/Header.css"
function Header() {
  return (
    <nav className="navbar navbar-expand-lg fixed-top shadow-sm py-3 headerContainer">
      <div className="container d-flex justify-content-between align-items-center">
        
        <a className="navbar-brand fs-3 fw-bold" href="/">AIBazaar</a>

        <form className="d-flex mx-auto w-50">
          <input
            className="form-control me-2"
            type="search"
            placeholder="Search items..."
            aria-label="Search"
          />
          <button className="btn btn-outline-success" type="submit">Search</button>
        </form>

        <div>
          <a href="/favorites" className="btn btn-success me-2">Favorites</a>
          <a href="/signup" className="btn btn-warning">Sign Up</a>
        </div>
      </div>
    </nav>
    
  );
}

export default Header;