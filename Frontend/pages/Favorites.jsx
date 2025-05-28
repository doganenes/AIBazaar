import React, { useState, useEffect } from "react";
import FavoriteProductCard from "../components/FavoriteProductCard";
import { Container, Row, Col, Pagination } from "react-bootstrap";
import { getAllFavoriteProducts, tokenToId } from "../api/api";

function Favorites() {
  const [favoriteProducts, setFavoriteProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
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

  return (
    <Container className="mt-4">
      <h2 className="mb-4 mt-3">My Favorite Products</h2>
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
              title={item.product.productName}
              description={item.product.description}
              imageUrl={item.product.imageUrl}
              link={`/product/${item.product.productID}`}
            />
          </Col>
        ))}
      </Row>

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
    </Container>
  );
}

export default Favorites;
