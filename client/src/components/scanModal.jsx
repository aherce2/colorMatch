import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import { useState } from 'react';

// Replace with response from device -> One Shot Mode
const modalTitle = [
  'Connect to Device First',
  'Place Device on Left Cheek',
  'Place Device on Right Cheek',
  'Place Device on Forehead',
  'Place Device on Chin',
  'Calculating Average and Monk Category ...' // Disappear after this and start process to get color data
];

const modalBody = [
  'Scanning ...',
  'Scan 1/4 Complete'
];

function ScanModal() {
  const [show, setShow] = useState(false); // Modal visibility state
  const [buttonVisible, setButtonVisible] = useState(true); // Button visibility state


  // start scan when button is pressed

  const handleShow = () => {
    setShow(true); // Show the modal
    setButtonVisible(false); // Hide the button when clicked
  };

  return (
    <div>
      {buttonVisible && (
        <Button
          variant="primary"
          onClick={handleShow}
          style={{ marginTop: '20px' }} 
        >
          Start Scan
        </Button>
      )}

      {show && (
        <div
          className="modal show"
          style={{ display: 'block', position: 'initial' }}
        >
          <Modal.Dialog>
            <Modal.Header>
              <Modal.Title>{modalTitle[1]}</Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <p>{modalBody[0]}</p>
            </Modal.Body>

            <Modal.Footer>
              <Button variant="primary" disabled>
                Next Step
              </Button>
            </Modal.Footer>
          </Modal.Dialog>
        </div>
      )}
    </div>
  );
}

export default ScanModal;
