import { useState, useEffect } from 'react'
import './App.css'
import DisplayCard   from './components/displayCard.jsx'
import ConnectBLE from './components/bleBTN.jsx'
import ScanModal from './components/scanModal.jsx'
import { socket } from './utils/socket'

function App() {
  useEffect(() => {
    // Connect socket
    socket.connect();

    // Log all initial messages
    socket.on('all_messages', (data) => {
      console.log('All messages:', data.messages);
    });

    // Log real-time updates
    socket.on('new_message', (data) => {
      console.log('New message:', data.message);
    });

    // Cleanup on component unmount
    return () => {
      socket.off('all_messages');
      socket.off('new_message');
      socket.disconnect();
    };
  }, []);

  return (
    <div className="App">
      <ConnectBLE/>
      <ScanModal/>
      {/* <DisplayCard /> */}
    </div>
  )
}

export default App
