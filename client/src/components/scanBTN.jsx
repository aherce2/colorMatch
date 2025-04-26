import React from 'react';

const ScanButton = ({ scanStatus,scanMessage, onStartScan, command  }) => {
  // return (
  //   <div className="d-grid gap-2 my-3">
  //     {/* <button className="btn btn-secondary" onClick={onStartScan}> */}
  //     <button className="btn btn-secondary" onClick={() => onStartScan(command)}>
  //       {command === '1'}
  //       {scanStatus === 'scanning' ? 'Scanning...' : 'One Shot Scan'}
  //     </button>
  //   </div>
  // );
  return (
    <div className="d-grid gap-2 my-3">
      <button className="btn btn-secondary" onClick={() => onStartScan(command)}>
        {scanStatus}
      </button>
      {command === '1'}
      <div>Status: {scanStatus}</div>
      {scanMessage && <div>Message: {scanMessage}</div>}
    </div>
  );
};

export default ScanButton;
