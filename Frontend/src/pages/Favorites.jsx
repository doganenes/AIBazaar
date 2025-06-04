import React, { useState, useEffect } from "react";
import FavoriteProductCard from "../components/FavoriteProductCard";
import { Container, Row, Col, Pagination } from "react-bootstrap";
import { getAllFavoriteProducts, tokenToId } from "../api/api";

function Favorites() {
  const [favoriteProducts, setFavoriteProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const itemsPerPage = 4;

  useEffect(() => {
    const fetchFavorites = async () => {
      try {
        const userId = await tokenToId();
        console.log("userId from token:", userId);
        const favorites = await getAllFavoriteProducts(userId);
        console.log("favorites response:", favorites);
        setFavoriteProducts(favorites);
      } catch (error) {
        console.error("Favorites not found:", error.message || error);
      } finally {
        setIsLoading(false);
      }
    };
    fetchFavorites();
  }, []);

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
      <Container className="mt-4">
        <h2 className="mb-4 mt-3">My Favorite Products</h2>
        <div className="text-center">Loading...</div>
      </Container>
    );
  }

  return (
    <Container className="mt-4">
      <h2 className="mb-4 mt-3">My Favorite Products</h2>

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
                  productID={item.product.productID}
                  title={item.product.productName}
                  description={item.product.description}
                  imageUrl={item.product.imageUrl}
                  link={`/product/${item.product.productID}`}
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
              {Array.from({ length: totalPages }, (_, index) => (
                <Pagination.Item
                  key={index + 1}
                  active={index + 1 === currentPage}
                  onClick={() => handlePageChange(index + 1)}
                >
                  {index + 1}
                </Pagination.Item>
              ))}
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
    </Container>
  );
}

export default Favorites;
