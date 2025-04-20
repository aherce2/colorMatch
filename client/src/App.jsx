import { useState } from 'react'
import './App.css'
import DisplayCard   from './components/displayCard.jsx'
import ConnectBLE from './components/bleBTN.jsx'
import ScanModal from './components/scanModal.jsx'
import MeasuredFigure from './components/measuredValue.jsx'
import useSocketEvents from './useSocketEvents.js'
import ImageUpload from './components/ImageUpload.jsx'

function App() {
  const [bleStatus, setBleStatus] = useState(false);
  const [products, setProducts] = useState([]);
  const [measuredValue, setMeasuredValue] = useState([0, 0, 0]);
  const [monk, setMonk] = useState([]);
  
  const { handleImageUpload } = useSocketEvents(setProducts, setMeasuredValue, setMonk, setBleStatus);

  // useSocketEvents(setProducts, setMeasuredValue,setMonk, setBleStatus);

  return (
    <div className="App">
      <ImageUpload handleImageUpload={handleImageUpload} />
      <ConnectBLE bleStatus={bleStatus} />
      <ScanModal/>
      <MeasuredFigure measuredValue={measuredValue} monk={monk}/>
      {products.length > 0 && <DisplayCard products={products} />}
    </div>
  )
}

export default App
