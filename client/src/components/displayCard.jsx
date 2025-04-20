import React, { useState, useEffect } from "react";
import { Container, Row, Col } from "react-bootstrap";
import CardComponent from "./card";



function DisplayCard({ products }) {
  return (
    <Container fluid className="mt-4">
      {products.length === 0 ? (
        <div className="text-center w-100 py-4">
          <h5>No products matching within threshold</h5>
        </div>
      ) : (
        <Row className="g-4">
          {products.map((product) => (
            <Col key={product.id} xs={3} sm={3} md={3} lg={3}>
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
      )}
    </Container>
  );
}

// function DisplayCard ({ products }) {
  
//   return (
//     <Container fluid className="mt-4">
//       <Row className="g-4">
//         {products.map((product) => (
//           <Col key={product.id} xs={12} md={6} lg={4}>
//             <CardComponent
//               swatch={product.hex}
//               brand={product.brand}
//               product={product.product}
//               shade={product.shade}
//               hex={product.hex}
//               percentMatch={product.percent_match}
//             />
//           </Col>
//         ))}
//       </Row>
//     </Container>
//   );
// }

export default DisplayCard
