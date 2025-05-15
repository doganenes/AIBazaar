import React, { useState } from 'react';
import FavoriteProductCard from '../components/FavoriteProductCard';
import { Container, Row, Col, Pagination } from 'react-bootstrap';

function Favorites() {
  const repeatedFavorites = Array.from({ length: 10 }, (_, index) => ({
    id: index + 1,
  }));

  const itemsPerPage = 4;
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(repeatedFavorites.length / itemsPerPage);

  // Şu anki sayfaya ait kartlar
  const currentItems = repeatedFavorites.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  return (
    <Container className="mt-4">
      <h2 className="mb-4">My Favorite Products</h2>
      <Row>
        {currentItems.map((item) => (
          <Col
            key={item.id}
            sm={12}
            md={6}
            lg={4}
            xl={3}
            className="mb-4 d-flex justify-content-center"
          >
            <FavoriteProductCard
              title="Card title"
              description="Some quick example text to build on the card title and make up the bulk of the card's content."
              imageUrl="project.jpg"
              link="#"
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
