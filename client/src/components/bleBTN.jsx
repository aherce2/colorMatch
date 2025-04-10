import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';

function ConnectBLE() {
  const [bleStatus, setBleStatus] = useState(false); // State to track BLE connection status
  const [showToast, setShowToast] = useState(false); // State to control toast visibility

  // Function to handle BLE connection toggle
  const toggleBleConnection = () => {
    const newStatus = !bleStatus;
    setBleStatus(newStatus);
    setShowToast(newStatus); // Show toast only when connected
  };
  useEffect(() => {
    let timer;
    if (showToast) {
      timer = setTimeout(() => {
        setShowToast(false);
      }, 2500); 
    }
    return () => clearTimeout(timer); // Cleanup timeout on unmount or state change
  }, [showToast]);

  return (
    <div className="d-grid gap-2">
      <Button onClick={toggleBleConnection} className="me-3">
        {bleStatus ? 'Disconnect Device' : 'Connect to Device'}
      </Button>
      {showToast && (
        <Toast onClose={() => setShowToast(false)} show={showToast} animation={false}>
          <Toast.Header>
            <Toast.Body>Successfully connected to the device!</Toast.Body>
          </Toast.Header>
          
        </Toast>
      )}
    </div>
  );
}

export default ConnectBLE;


  
// function ConnectBLE() {
//   const [bleStatus, setBleStatus] = useState(false); // State to track BLE connection status

//   // Function to handle button press -> Modify for axios BLE Connection
//   const handleButtonClick = () => {
//     setBleStatus(!bleStatus); // Toggle the BLE status
//   };

//   // Determine the text to display based on bleStatus
//   const buttonVariant = bleStatus ? 'primary' : 'outline-primary';
//   const buttonText = bleStatus
//     ? 'Connected to Device'
//     : 'Press to Connect to Device';

//   return (
//     <div className="d-grid gap-2">
//       <Button variant={buttonVariant} size="lg" onClick={handleButtonClick}>
//         {buttonText}
//       </Button>
//     </div>
//   );
// }

// export default ConnectBLE;
