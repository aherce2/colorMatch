import { useEffect, useCallback  } from 'react';
import { socket } from './utils/socket'

const useSocketEvents = (setProducts, setMeasuredValue, setMonk, setBleStatus) => {
  
  const handleImageUpload = useCallback(async (file) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const buffer = reader.result;
      socket.emit('analyze_input', { filename: file.name }, buffer);
    };
    reader.readAsArrayBuffer(file);
  }, []);

  useEffect(() => {
    socket.connect();

    const socketEventHandlers = {
      'upload_error': (error) => console.error('Upload failed:', error),
      'lab_products': (data) => setProducts(data.products || 'No Products Available'),
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
  }, [setProducts, setMeasuredValue, setMonk, setBleStatus]);
  return { handleImageUpload };
};

export default useSocketEvents;