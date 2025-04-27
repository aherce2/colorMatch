
import React from 'react';

const MultiScan = ({ scanStatus, onStartScan, command  }) => {

  return (
    <div className="d-grid gap-2 my-3">
      <button className="btn btn-info" onClick={() => onStartScan(command)}>
      {scanStatus}
      </button>
      {command === '0'}
    </div>
  );
};

export default MultiScan;
