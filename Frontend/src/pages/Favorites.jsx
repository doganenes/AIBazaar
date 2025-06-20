import React, { useState, useEffect } from "react";
import FavoriteProductCard from "../components/FavoriteProductCard";
import {
  Container,
  Row,
  Col,
  Pagination,
  Toast,
  ToastContainer,
} from "react-bootstrap";
import { getAllFavoriteProducts, tokenToId } from "../api/api";
import "../css/Favorites.css";

function Favorites() {
  const [favoriteProducts, setFavoriteProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const itemsPerPage = 4;

  const [toast, setToast] = useState({
    show: false,
    message: "",
    variant: "success",
  });

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const userId = await tokenToId();
        const favorites = await getAllFavoriteProducts(userId);
        setFavoriteProducts(favorites);
      } catch (error) {
        console.error("Favorites not found:", error.message || error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchFavorites();
  }, []);

  const showToast = (message, variant = "danger") => {
    setToast({ show: true, message, variant });
    setTimeout(() => {
      setToast((prev) => ({ ...prev, show: false }));
    }, 3000);
  };

  const handleRemoveFavorite = (productId) => {
    setFavoriteProducts((prev) =>
      prev.filter((item) => item.product.productID !== productId)
    );
    const newTotalPages = Math.ceil(
      (favoriteProducts.length - 1) / itemsPerPage
    );
    if (currentPage > newTotalPages && newTotalPages > 0) {
      setCurrentPage(newTotalPages);
    }
  };

  const totalPages = Math.ceil(favoriteProducts.length / itemsPerPage);
  const currentItems = favoriteProducts.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  if (isLoading) {
    return (
      <Container className="mt-5">
        <div className="text-center">Loading...</div>
      </Container>
    );
  }

  return (
    <Container className="favorites-container">
      {favoriteProducts.length > 0 && (
        <h2 className="mb-5 mt-3">My Favorite Products</h2>
      )}

      {favoriteProducts.length === 0 ? (
        <div className="text-center mt-5">
          <h4>No favorite products found</h4>
          <p className="text-muted">
            You haven't added any products to your favorites yet.
          </p>
        </div>
      ) : (
        <>
          <Row>
            {currentItems.map((item) => (
              <Col
                key={item.favoriteProductID}
                sm={12}
                md={6}
                lg={4}
                xl={3}
                className="mb-4 d-flex justify-content-center"
              >
                <FavoriteProductCard
                  key={item.product.productID}
                  productID={item.product.productID}
                  title={item.product.productName}
                  description={item.product.description}
                  imageUrl={item.product.imageUrl}
                  price={item.product.price}
                  link={`/product/${item.product.productID}`}
                  onFavoriteRemoved={(message, type) => {
                    showToast(message, type);
                    handleRemoveFavorite(item.product.productID);
                  }}
                />
              </Col>
            ))}
          </Row>

          {totalPages > 1 && (
            <Pagination className="justify-content-center mt-4">
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
                  <Pagination.Item onClick={() => handlePageChange(totalPages)}>
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
          )}
        </>
      )}
      <ToastContainer
        position="bottom-start"
        className="p-3"
        style={{ zIndex: 9999 }}
      >
        <Toast
          show={toast.show}
          onClose={() => setToast((prev) => ({ ...prev, show: false }))}
          delay={3000}
          bg={toast.variant}
        >
          <Toast.Header closeButton>
            <strong className="me-auto">
              {toast.variant === "success" ? "Success" : "Fail"}
            </strong>
          </Toast.Header>
          <Toast.Body className="text-white">{toast.message}</Toast.Body>
        </Toast>
      </ToastContainer>
    </Container>
  );
}

export default Favorites;