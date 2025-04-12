import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import CardComponent from "./card";
import axios from "axios";

function DisplayCard () {
  const [error, setError] = useState(null);
  const [products, setProducts] = useState([]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get("http://localhost:8080/api/products");
      return response.data; // Return the response data directly
    } catch (error) {
      console.error("Error fetching products:", error);
      return { success: false, message: "Failed to fetch products" };
    }
  };

  useEffect(() => {
    const getProducts = async () => {
      const result = await fetchProducts();
      if (result.success === false) {
        setError(result.message);
      } else if (Array.isArray(result) && result.length === 0) {
        setError("Sorry, No matches available within Appropriate Threshold.");
      } else {
        setProducts(result);
      }
    };
    getProducts();
  }, []);


  if (error) {
    return <div style={{ textAlign: "center", marginTop: "2rem" }}>{error}</div>;
  }

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
