import { useState, useEffect } from 'react'
import './App.css'
import DisplayCard   from './components/displayCard.jsx'
import ConnectBLE from './components/bleBTN.jsx'
import ScanModal from './components/scanModal.jsx'
import FigureExample from './components/measuredValue.jsx'
import useSocketEvents from './useSocketEvents.js'
import { socket } from './utils/socket'

function App() {
  const [products, setProducts] = useState([]);
  const [measuredValue, setMeasuredValue] = useState([0, 0, 0]);

  useSocketEvents(setProducts, setMeasuredValue);
  
  return (
    <div className="App">
      <ConnectBLE/>
      <ScanModal/>
      <FigureExample/>
      {/* <FigureExample measuredValue={measuredValue} /> */}
      {products.length > 0 && <DisplayCard products={products} />}
    </div>
  )
}

export default App
