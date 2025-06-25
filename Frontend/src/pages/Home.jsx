import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import { getAllProducts } from "../api/api";
import "bootstrap/dist/css/bootstrap.min.css";
import "../css/Home.css";
import { ToastContainer, Toast, Pagination } from "react-bootstrap";

const Home = ({ searchTerm }) => {
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 12;

  const [toast, setToast] = useState({
    show: false,
    message: "",
    type: "success",
  });

  const [filteredProducts, setFilteredProducts] = useState([]);

  useEffect(() => {
    getAllProducts()
      .then((data) => {
        setProducts(data);
        setFilteredProducts(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error loading products:", err);
        setLoading(false);
      });
  }, []);

  const showToast = (message, type = "success") => {
    setToast({ show: true, message, type });
  };

  useEffect(() => {
    const filtered = products.filter(
      (product) =>
        product.productName?.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredProducts(filtered);
    setCurrentPage(1);
  }, [searchTerm, products]);

  const totalPages = Math.ceil(filteredProducts.length / itemsPerPage);
  const currentItems = filteredProducts.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (loading) {
    return (
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ minHeight: "100vh", backgroundColor: "#ffffff" }}
      >
        <div className="text-center text-dark">
          <div
            className="spinner-border mb-3"
            role="status"
            style={{ width: "4rem", height: "4rem" }}
          >
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        backgroundColor: "#ffffff",
        paddingTop: "100px",
      }}
    >
      <div className="container py-4">
        <div className="row mb-4">
          <div className="col-md-8"></div>
          <div className="col-md-4 text-md-end">
            <span className="badge bg-dark rounded text-white fs-6 px-3 py-2">
              {filteredProducts.length}{" "}
              {filteredProducts.length === 1 ? "Product" : "Products"}
            </span>
          </div>
        </div>

        {filteredProducts.length === 0 ? (
          <div className="row justify-content-center">
            <div className="col-md-6 text-center">
              <div className="bg-light rounded p-5 shadow-sm">
                <div className="mb-4">
                  <i className="fas fa-search fa-4x text-muted"></i>
                </div>
                <h3 className="h4 text-dark mb-3">
                  {searchTerm ? "No products found" : "No products yet"}
                </h3>
                <p className="text-muted mb-4">
                  {searchTerm
                    ? "Try different keywords to search again"
                    : "New products will be added soon"}
                </p>
                {searchTerm && (
                  <button
                    onClick={() => setSearchTerm("")}
                    className="btn btn-outline-dark btn-lg"
                  >
                    Clear Search
                  </button>
                )}
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="row g-4">
              {currentItems.map((product, index) => (
                <div
                  key={product.productID || index}
                  className="col-lg-3 col-md-4 col-sm-6"
                  style={{
                    animationDelay: `${index * 100}ms`,
                    animation: "fadeInUp 0.8s ease-out forwards",
                    opacity: 0,
                  }}
                >
                  <ProductCard
                    product={product}
                    onFavoriteAdded={(message, type) =>
                      showToast(message, type)
                    }
                  />
                </div>
              ))}
            </div>

            {totalPages > 1 && (
              <div className="d-flex justify-content-center mt-5">
                <Pagination>
                  <Pagination.First
                    onClick={() => handlePageChange(1)}
                    disabled={currentPage === 1}
                  />
                  <Pagination.Prev
                    onClick={() => handlePageChange(currentPage - 1)}
                    disabled={currentPage === 1}
                  />

                  {currentPage > 2 && (
                    <>
                      <Pagination.Item onClick={() => handlePageChange(1)}>
                        1
                      </Pagination.Item>
                      {currentPage > 3 && <Pagination.Ellipsis disabled />}
                    </>
                  )}

                  {currentPage > 1 && (
                    <Pagination.Item
                      onClick={() => handlePageChange(currentPage - 1)}
                    >
                      {currentPage - 1}
                    </Pagination.Item>
                  )}

                  <Pagination.Item active>{currentPage}</Pagination.Item>

                  {currentPage < totalPages && (
                    <Pagination.Item
                      onClick={() => handlePageChange(currentPage + 1)}
                    >
                      {currentPage + 1}
                    </Pagination.Item>
                  )}

                  {currentPage < totalPages - 1 && (
                    <>
                      {currentPage < totalPages - 2 && (
                        <Pagination.Ellipsis disabled />
                      )}
                      <Pagination.Item
                        onClick={() => handlePageChange(totalPages)}
                      >
                        {totalPages}
                      </Pagination.Item>
                    </>
                  )}

                  <Pagination.Next
                    onClick={() => handlePageChange(currentPage + 1)}
                    disabled={currentPage === totalPages}
                  />
                  <Pagination.Last
                    onClick={() => handlePageChange(totalPages)}
                    disabled={currentPage === totalPages}
                  />
                </Pagination>
              </div>
            )}
          </>
        )}
      </div>
      <ToastContainer
        className="p-3"
        style={{
          zIndex: 9999,
          position: "fixed",
          bottom: "1rem",
          left: "1rem",
        }}
      >
        <Toast
          show={toast.show}
          onClose={() => setToast((prev) => ({ ...prev, show: false }))}
          delay={3000}
          autohide
          bg={toast.type === "success" ? "success" : "danger"}
        >
          <Toast.Header closeButton>
            <strong className="me-auto">
              {toast.type === "success" ? "success" : "Fail"}
            </strong>
          </Toast.Header>
          <Toast.Body className="text-white">{toast.message}</Toast.Body>
        </Toast>
      </ToastContainer>
    </div>
  );
};

export default Home;
