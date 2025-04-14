// src/hooks/useSocketEvents.js
import { useEffect } from 'react';
import { socket } from './utils/socket'

const useSocketEvents = (setProducts, setMeasuredValue, setMonk) => {
  useEffect(() => {
    socket.connect();

    const socketEventHandlers = {
      'lab_products': (data) => setProducts(data.products || 'No Products Available'),
      'target_lab': (data) => setMeasuredValue?.(data.target || [0, 0, 0]),
      'monk_category': (data) => setMonk?.(data.monk_category || 'No categories available'),
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
  }, [setProducts, setMeasuredValue]);
};

export default useSocketEvents;