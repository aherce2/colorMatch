/*

Function to Handle Bluetooth Connection Button feedback with device with Python Backend communication

*/

import axios from 'axios';
import { useState, useEffect } from 'react';

function useConnectBLE() {
  const [bleStatus, setBleStatus] = useState(false); // State to track BLE connection status
  const [showToast, setShowToast] = useState(false); // State to control toast visibility
  const [toastText, setToastText] = useState(''); // State to store dynamic toast text

  // Button text based on BLE connection status
  const buttonText = bleStatus
    ? 'Press to Disconnect Device'
    : 'Press to Connect to Device';
    
    // Handle AXIOS Request
    const handleBLE = async (status) => {
        try {
            const response = await axios.get(`http://localhost:8080/api/ble/${status}`);
            return response.data; // Return the response data directly
        } catch (error) {
            console.error('Error during Axios GET call:', error);
            return { success: false, message: 'Failed to connect to BLE device' };
        }
    };

  // Function to handle button click
  const handleOnClick = async () => {
    try {
      const result = await handleBLE(`${bleStatus}`);
      if (result.success) {
        setBleStatus(!bleStatus); // Toggle BLE connection status on success
        setToastText(result.message); // Set toast text based on backend response
        setShowToast(true); // Show toast on success
      } else {
        console.error(result.message || 'Error occurred while connecting/disconnecting BLE');
      }
    } catch (error) {
      console.error('Error during BLE connection:', error);
    }
  };

  useEffect(() => {
    let timer;
    if (showToast) {
      timer = setTimeout(() => {
        setShowToast(false);
      }, 2500);
    }
    return () => clearTimeout(timer); // Cleanup timeout on unmount or state change
  }, [showToast]);

  return { handleOnClick, buttonText, showToast, toastText, setShowToast };
}

export default useConnectBLE;
