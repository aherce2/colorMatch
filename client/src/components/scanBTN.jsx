import React from 'react';

const ScanButton = ({scanMessage, onStartScan, command, disabled  }) => {

  return (
    <div className="d-grid gap-2 my-3">
      <button className="btn btn-secondary" onClick={() => onStartScan(command)} disabled={disabled}>
      {scanMessage}
      </button>
      {command === '1'}
    </div>
  );
};

export default ScanButton;
