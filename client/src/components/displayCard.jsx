import React from "react";
import { Container, Row, Col } from "react-bootstrap";
import CardComponent from "./card";

const cardsData = [
  { id: 1, brand: "Brand 1", product: "Product 1", shade: "Shade 1", hex: "#3498db" },
  { id: 2, brand: "Brand 2", product: "Product 2", shade: "Shade 2", hex: "#e74c3c" },
  { id: 3, brand: "Brand 3", product: "Product 3", shade: "Shade 3", hex: "#2ecc71" },
  { id: 4, brand: "Brand 4", product: "Product 4", shade: "Shade 4", hex: "#f1c40f" }

];

function DisplayCard () {
  return (
    <Container fluid className="mt-4">
      <Row className="g-4">
        {cardsData.map((card) => (
          <Col key={card.id} xs={12} sm={6} md={4} lg={3}>
            <CardComponent
              swatch={card.hex}
              brand={card.brand}
              product={card.product}
              shade={card.shade}
              hex={card.hex}
            />
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default DisplayCard
