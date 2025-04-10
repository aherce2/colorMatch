import { useState } from 'react'
import { useState } from 'react'
import './App.css'
import DisplayCard   from './components/displayCard.jsx'
import ConnectBLE from './components/bleBTN.jsx'
import ScanModal from './components/scanModal.jsx'


function App() {
  
  return (
    <div className="App">
      <ConnectBLE/>
      <ScanModal/>
      {/* <DisplayCard /> */}
    </div>
  )
}

export default App
