import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';


//Replace with response from device -> One Shot Mode

const modalTitle = [
    'Place Device on Left Cheek',
    'Place Device on Right Cheek',
    'Place Device on Forhead',
    'Place Device on Chin',
    'Calculating Average and Monk Category ...' //Disappear after this and start process to get color data
]

const modalBody = [
    'Scanning ...',
    'Scan 1/4 Complete'
]

function ScanModal() {
  return (
    <div
      className="modal show"
      style={{ display: 'block', position: 'initial' }}
    >
      <Modal.Dialog>
        <Modal.Header closeButton>
          <Modal.Title>{modalTitle[0]}</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          <p>{modalBody[0]}</p>
        </Modal.Body>

        <Modal.Footer>
          <Button variant="primary" disabled>Next Step</Button>
        </Modal.Footer>

      </Modal.Dialog>
    </div>
  );
}

export default ScanModal;