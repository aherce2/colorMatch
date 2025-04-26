import React from 'react';

const ScanButton = ({ scanStatus, onStartScan,command  }) => {
  return (
    <div className="d-grid gap-2 my-3">
      {/* <button className="btn btn-secondary" onClick={onStartScan}> */}
      <button className="btn btn-secondary" onClick={() => onStartScan(command)}>
        {command === '1' ? 'Start Scan' : 'Stop Scan'}
        {/* {scanStatus === 'scanning' ? 'Scanning...' : 'One Shot Scan'} */}
      </button>
    </div>
  );
};

export default ScanButton;
