import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import CardComponent from "./card";
import axios from "axios";

// const cardsData = [
//   { id: 1, brand: "Brand 1", product: "Product 1", shade: "Shade 1", hex: "#3498db" },
//   { id: 2, brand: "Brand 2", product: "Product 2", shade: "Shade 2", hex: "#e74c3c" },
//   { id: 3, brand: "Brand 3", product: "Product 3", shade: "Shade 3", hex: "#2ecc71" },
//   { id: 4, brand: "Brand 4", product: "Product 4", shade: "Shade 4", hex: "#f1c40f" }

// ];

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
        setError(result.message); // Set error message
      } else {
        setProducts(result); // Set fetched products
      }
    };
    getProducts();
  }, []);

  if (error) {
    return <div>Error: {error}</div>; // Display error message
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
