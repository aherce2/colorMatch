import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import CardComponent from "./card";
import axios from "axios";
import { socket } from '../utils/socket'

function DisplayCard ({ products }) {
  // const [products, setProducts] = useState([]);
  
  // useEffect(() => {
  //   socket.on('lab_products', (data) => {
  //     setProducts(data.products);
  //   });
  
  //   return () => {
  //     socket.off('lab_products');
  //   };
  // }, []);
  
  return (
    <Container fluid className="mt-4">
      <Row className="g-4">
        {products.map((product) => (
          <Col key={product.id} xs={12} md={6} lg={4}>
            <CardComponent
              swatch={product.hex}
              brand={product.brand}
              product={product.product}
              shade={product.shade}
              hex={product.hex}
              percentMatch={product.percent_match}
            />
          </Col>
        ))}
      </Row>
    </Container>
  );
}

export default DisplayCard
