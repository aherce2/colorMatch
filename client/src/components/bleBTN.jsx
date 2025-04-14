import React from 'react';
import Button from 'react-bootstrap/Button';
import Toast from 'react-bootstrap/Toast';
import useConnectBLE from '../connectBle';

  function ConnectBLE({bleStatus}) {
  const { 
    handleOnClick, 
    buttonText, 
    showToast, 
    toastText 
  } = useConnectBLE();

  return (
    <div className="d-grid gap-2">
      <Button 
        variant={bleStatus ? 'danger' : 'primary'} 
        onClick={handleOnClick}
      >
        {buttonText}
      </Button>
      
      <Toast show={showToast} onClose={() => setShowToast(false)} delay={3000} autohide>
        <Toast.Header className="bg-light">
          <strong className="me-auto">{toastText}</strong>
        </Toast.Header>
      </Toast>
    </div>
  );
}

export default ConnectBLE;
