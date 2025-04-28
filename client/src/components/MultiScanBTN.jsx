
import React from 'react';

const MultiScan = ({ scanStatus, onStartScan, command, disabled  }) => {

  return (
    <div className="d-grid gap-2 my-3">
      <button className="btn btn-info" onClick={() => onStartScan(command)} disabled={disabled}>
      {scanStatus}
      </button>
      {command === '0'}
    </div>
  );
};

export default MultiScan;
