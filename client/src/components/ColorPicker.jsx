import { useState } from 'react';
import Form from 'react-bootstrap/Form';

function ColorPicker({ onColorSelect }) {
  const [color, setColor] = useState('#000000');

  const handleChange = (e) => {
    const hex = e.target.value;
    setColor(hex);
    onColorSelect(hex);
  };

  return (
    <>
      <Form.Control
        type="color"
        value={color}
        title="Choose your color"
        onChange={handleChange}
        style={{ width: 60, height: 60, padding: 0, borderRadius: 8 }}
      />
    </>
  );
}

export default ColorPicker;
