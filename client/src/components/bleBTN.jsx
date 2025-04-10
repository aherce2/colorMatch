import React from 'react';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';
import useConnectBLE from '../connectBle'; 

function ConnectBLE() {
  
  const { 
    handleOnClick, 
    buttonText, 
    showToast, 
    toastText, 
    setShowToast 
  } = useConnectBLE(); // Custom Hook

  return (
    <div className="d-grid gap-2">
      <Button onClick={handleOnClick} className="me-3">
        {buttonText}
      </Button>
      {showToast && (
        <Toast onClose={() => setShowToast(false)} show={showToast} animation={false}>
          <Toast.Header>
            <strong className="me-auto">{toastText}</strong>
          </Toast.Header>
        </Toast>
      )}
    </div>
  );
}

export default ConnectBLE;
