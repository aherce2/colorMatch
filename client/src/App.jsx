import { useState } from 'react'
import './App.css'
import DisplayCard   from './components/displayCard.jsx'
import ConnectBLE from './components/bleBTN.jsx'
import MeasuredFigure from './components/measuredValue.jsx'
import useSocketEvents from './useSocketEvents.js'
import ImageUpload from './components/ImageUpload.jsx'
import ColorPicker from './components/ColorPicker.jsx'
import ScanButton from './components/scanBTN.jsx';
import MultiScan from './components/MultiScanBTN.jsx'

function App() {
  const [bleStatus, setBleStatus] = useState(false);
  const [products, setProducts] = useState([]);
  const [measuredValue, setMeasuredValue] = useState([0, 0, 0]);
  const [monk, setMonk] = useState([]);
  const [scanStatus, setScanStatus] = useState('Start Scan with Lighting');
  const [scanMessage, setScanMessage] = useState('Start Scan');


  const { handleImageUpload, handleColorSelect, handleStartScan } = useSocketEvents(
    setProducts,
    setMeasuredValue,
    setMonk,
    setBleStatus,
    setScanStatus,
    setScanMessage
  );
  
  return (
    <div className="App">

      {!bleStatus &&
        <div className="top-bar">
          <ColorPicker onColorSelect={handleColorSelect} />
          <ImageUpload handleImageUpload={handleImageUpload} />
        </div>
      }

      <ConnectBLE bleStatus={bleStatus} />
      {/* Conditionally Show ScanModal if BLE is connnected */}


      <MultiScan 
        onStartScan={handleStartScan} 
        command="0" 
        scanStatus={scanStatus}
      />

      <ScanButton 
        onStartScan={handleStartScan} 
        command="1" 
        scanMessage={scanMessage}
      />
      <MeasuredFigure measuredValue={measuredValue} monk={monk}/>
      {/* {bleStatus && products.length > 0 && <DisplayCard products={products}/>} */}

      {(
        products.length > 0 ? (
          <DisplayCard products={products} />
        ) : (<h5>No products matching within threshold</h5>)
      )}
      
    </div>
  )
}

export default App
