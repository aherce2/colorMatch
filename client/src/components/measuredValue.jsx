import { useState, useEffect } from 'react'
import { Figure } from 'react-bootstrap';
import { socket } from '../utils/socket'

function FigureExample() {
  const [measuredValue, setMeasuredValue] = useState([0, 0, 0]); 

  useEffect(() => {
    socket.on('target_lab', (data) => {
      setMeasuredValue(data.target); // data.target now has both rgb and hex
    });
  
    return () => {
      socket.off('target_lab');
    };
  }, []);
  
  const rgbColor = `rgb(${measuredValue.rgb?.join(',') || '0,0,0'})`;
  const hexColor = measuredValue.hex || '#000000';
  

  return (
    <Figure>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '16px',
        }}
      >
        <div
          style={{
            backgroundColor: rgbColor,
            width: '200px',
            aspectRatio: '1 / 1',
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
            {hexColor}
          </span>
        </div>
      </div>
      <Figure.Caption>
        Measured Skin Color
      </Figure.Caption>
    </Figure>
  );
}

export default FigureExample;
