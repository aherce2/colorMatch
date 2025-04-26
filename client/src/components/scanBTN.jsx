import React from 'react';

const ScanButton = ({ scanStatus,scanMessage, onStartScan, command  }) => {

  return (
    <div className="d-grid gap-2 my-3">
      <button className="btn btn-secondary" onClick={() => onStartScan(command)}>
      {scanMessage}
      </button>
      {command === '1'}
    </div>
  );
};

export default ScanButton;
