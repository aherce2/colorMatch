
import { useEffect, useCallback, useState } from 'react';
import { socket } from './utils/socket';

const useSocketEvents = (setProducts, setMeasuredValue, setMonk, setBleStatus, setScanStatus) => {


  // const handleStartScan = useCallback(() => {
  //   if (socket.connected) {
  //     setScanStatus('scanning');
  //     socket.emit('start_scan');
  //     setTimeout(() => setScanStatus('complete'), 3000);
  //   }
  // }, [setScanStatus]);
  const handleStartScan = useCallback((command) => {
    if (socket.connected) {
      console.log("Button Clicked Successfully");
      setScanStatus('scanning');
      socket.emit('start_scan', { command }); // Send command to backend
      setTimeout(() => setScanStatus('complete'), 3000);
    }
  }, [setScanStatus]);


  const handleImageUpload = useCallback(async (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const buffer = reader.result;
      socket.emit('analyze_input', { filename: file.name }, buffer);
    };
    reader.readAsArrayBuffer(file);
  }, []);

  const handleColorSelect = useCallback((hexColor) => {
    const r = parseInt(hexColor.slice(1, 3), 16);
    const g = parseInt(hexColor.slice(3, 5), 16);
    const b = parseInt(hexColor.slice(5, 7), 16);
    socket.emit('analyze_input', { color: true, rgb: [r, g, b] }, null);
  }, []);


  useEffect(() => {
    socket.connect();

    const socketEventHandlers = {
      'scan_status': (data) => {
        setScanStatus(data.status);
        if (data.status === 'acknowledged') {
          setTimeout(() => setScanStatus('complete'), 2500);
        }
      },
      'upload_error': (error) => console.error('Upload failed:', error),
      'lab_products': (data) => setProducts(data.products),
      'target_lab': (data) => setMeasuredValue?.(data.target || [0, 0, 0]),
      'monk_category': (data) => setMonk?.(data.monk_category || 'No categories available'),
      'ble_status': (data) => {
        setBleStatus?.(data.status === 'connected');
        if (data.status === 'error') {
          console.error('BLE Error:', data.message);
        }
      }
    };

    // Attach handlers
    Object.entries(socketEventHandlers).forEach(([event, handler]) => {
      socket.on(event, handler);
    });

    // Cleanup
    return () => {
      Object.keys(socketEventHandlers).forEach((event) => {
        socket.off(event);
      });
      socket.disconnect();
    };
  }, [setProducts, setMeasuredValue, setMonk, setBleStatus,setScanStatus]);

  return { 
    handleImageUpload, 
    handleColorSelect,
    handleStartScan
  };
};

export default useSocketEvents;