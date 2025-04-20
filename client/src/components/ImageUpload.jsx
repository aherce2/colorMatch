import Form from 'react-bootstrap/Form';
import useSocketEvents from '../useSocketEvents.js'

const ImageUpload = ({ handleImageUpload }) => {


  return (
    <Form.Group controlId="formFile" className="mb-3">
      <Form.Label>Upload Image</Form.Label>
      <Form.Control 
        type="file"
        accept="image/*"
        onChange={(e) => e.target.files?.[0] && handleImageUpload(e.target.files[0])}
      />
    </Form.Group>
  );
};

export default ImageUpload;


