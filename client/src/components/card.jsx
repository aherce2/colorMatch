import Card from 'react-bootstrap/Card';
import ListGroup from 'react-bootstrap/ListGroup';

function CardComponent({ swatch, brand, product, shade, hex, percentMatch }) {
  return (
    <Card className="h-100">
    {/* <Card style={{ width: '18rem' }}> */}
      {/* <div
        style={{
          backgroundColor: swatch,
          height: '180px',
          width: '100%',
          position: 'relative', 
        }}
      > */}
      <div
        style={{
          backgroundColor: swatch,
          height: '180px',
          width: '100%',
          position: 'relative', 
        }}
      >
        <span
          style={{
            position: 'absolute',
            bottom: '10px', 
            right: '10px', 
            backgroundColor: 'rgba(255, 255, 255, 0.7)', 
            padding: '2px 5px', 
            borderRadius: '3px', 
            fontSize: '12px', 
            fontWeight: 'bold', 
          }}
        >
          {hex}
        </span>
      </div>
      <Card.Body>
        <Card.Title>{brand}</Card.Title>
        <Card.Text></Card.Text>
      </Card.Body>
      <ListGroup className="list-group-flush">
        <ListGroup.Item>
          <span style={{ fontWeight: 'bold' }}>Product:</span> {product}
        </ListGroup.Item>
        <ListGroup.Item>
          <span style={{ fontWeight: 'bold' }}>Shade:</span> {shade}
        </ListGroup.Item>
        <ListGroup.Item>
          <span style={{ fontWeight: 'bold' }}>Match Percentage:</span> {percentMatch}
        </ListGroup.Item>
      </ListGroup>
    </Card>
  );
}

export default CardComponent;
