import { useState } from 'react'
import './App.css'
import DisplayCard   from './components/displayCard.jsx'
import ConnectBLE from './components/bleBTN.jsx'
import ScanModal from './components/scanModal.jsx'
import MeasuredFigure from './components/measuredValue.jsx'
import useSocketEvents from './useSocketEvents.js'
import ImageUpload from './components/ImageUpload.jsx'
import ColorPicker from './components/ColorPicker.jsx'

function App() {
  const [bleStatus, setBleStatus] = useState(false);
  const [products, setProducts] = useState([]);
  const [measuredValue, setMeasuredValue] = useState([0, 0, 0]);
  const [monk, setMonk] = useState([]);
    
  const { handleImageUpload, handleColorSelect  } = useSocketEvents(setProducts, setMeasuredValue, setMonk, setBleStatus);

  return (
    <div className="App">
      {/* <div className="top-bar">
        <ColorPicker onColorSelect={handleColorSelect} />
        <ImageUpload handleImageUpload={handleImageUpload} />
      </div> */}

      {!bleStatus &&
        <div className="top-bar">
          <ColorPicker onColorSelect={handleColorSelect} />
          <ImageUpload handleImageUpload={handleImageUpload} />
        </div>
      }

      <ConnectBLE bleStatus={bleStatus} />
      {/* <ScanModal/> */}
      {/* Conditionally Show ScanModal if BLE is connnected */}
      
      {bleStatus && <ScanModal />} 
      <MeasuredFigure measuredValue={measuredValue} monk={monk}/>
      <DisplayCard products={products}/>
    </div>
  )
}

export default App
