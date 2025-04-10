import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

// const swatch = '#3498db';
// const brand = 'brand name';
// const product = 'product name';
// const shade = 'shade name';
// const hex = 'hex value';

function CardComponent({ swatch, brand, product, shade, hex }) {
  return (
    <Card style={{ width: '18rem' }}>
      <div
        style={{
          backgroundColor: swatch, 
          height: '180px',
          width: '100%', 
        }}
      ></div>
      <Card.Body>
        <Card.Title>{brand}</Card.Title>
        <Card.Text>
        </Card.Text>
      </Card.Body>
      <ListGroup className="list-group-flush">
        {/* <ListGroup.Item>Product: {product}</ListGroup.Item> */}
        <ListGroup.Item>
          <span style={{ fontWeight: 'bold' }}>Product:</span> {product}
        </ListGroup.Item>

        <ListGroup.Item>
          <span style={{ fontWeight: 'bold' }}>Shade:</span> {shade}
        </ListGroup.Item>
        <ListGroup.Item>{hex}</ListGroup.Item>
        
      </ListGroup>
    </Card>
  );
}

export default CardComponent;