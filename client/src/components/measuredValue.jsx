import React from 'react';
import { Figure } from 'react-bootstrap';

function MeasuredFigure({ measuredValue, monk }) {
  const rgbColor = `rgb(${measuredValue.rgb?.join(',') || '0,0,0'})`;
  const hexColor = measuredValue.hex || '#000000';

  return (
    <Figure>
      <Figure.Caption
        style={{
          padding: '8px 16px',
          textAlign: 'center',
        }}
      >
        Measured Skin Color
      </Figure.Caption>
      <div
        style={{
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
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
      <Figure.Caption
        style={{
          padding: '8px 16px',
          textAlign: 'center',
        }}
      >
        Closest Monk Category: {monk}
      </Figure.Caption>
    </Figure>
  );
}

export default MeasuredFigure;
