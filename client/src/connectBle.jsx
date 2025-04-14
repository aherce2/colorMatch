/*

Function to Handle Bluetooth Connection Button feedback with device with Python Backend communication

*/

import { useState, useEffect } from 'react';
import { socket } from '../src/utils/socket'; 

function useConnectBLE() {
  const [bleStatus, setBleStatus] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastText, setToastText] = useState('');

  const buttonText = bleStatus 
    ? 'Disconnect BLE Device'
    : 'Connect BLE Device';

  useEffect(() => {
    const handleBLEStatus = (data) => {
      setToastText(data.message);
      setShowToast(true);
      
      if (data.status === 'connected') {
        setBleStatus(true);
      } else if (data.status === 'disconnected') {
        setBleStatus(false);
      }
    };

    socket.on('ble_status', handleBLEStatus);
    return () => socket.off('ble_status', handleBLEStatus);
  }, []);

  // Handle connection toggle
  const handleOnClick = () => {
    if (bleStatus) {
      socket.emit('ble_disconnect');
    } else {
      socket.emit('ble_connect');
    }
  };

  // Toast autohide
  useEffect(() => {
    const timer = showToast && setTimeout(() => setShowToast(false), 2500);
    return () => timer && clearTimeout(timer);
  }, [showToast]);

  return { handleOnClick, buttonText, showToast, toastText, setShowToast };
}
export default useConnectBLE;
