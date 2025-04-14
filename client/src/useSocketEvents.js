// src/hooks/useSocketEvents.js
import { useEffect } from 'react';
import { socket } from '../utils/socket';

const useSocketEvents = (setProducts, setMeasuredValue) => {
  useEffect(() => {
    socket.connect();

    const socketEventHandlers = {
      'lab_products': (data) => setProducts(data.products || []),
      'target_lab': (data) => setMeasuredValue?.(data.target || [0, 0, 0]),
      'new_message': (data) => console.log('New message:', data.message),
      'all_messages': (data) => console.log('All messages:', data.messages),
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


    /*
    
  useEffect(() => {
    // Define event handlers in a dictionary
    const socketEventHandlers = {
      'lab_products': (data) => setProducts(data.products || []),
      'target_lab': (data) => setMeasuredValue(data.target || [0, 0, 0]),
      'new_message': (data) => console.log('New message:', data.message),
      'all_messages': (data) => console.log('All messages:', data.messages),
    };

    // Attach all event handlers dynamically
    Object.entries(socketEventHandlers).forEach(([event, handler]) => {
      socket.on(event, handler);
    });

    // Cleanup: Detach all event handlers dynamically
    return () => {
      Object.keys(socketEventHandlers).forEach((event) => {
        socket.off(event);
      });
      socket.disconnect();
    };
  }, []);

    
  useEffect(() => {
    // Connect socket
    socket.connect();

    // // Log all initial messages
    // socket.on('all_messages', (data) => {
    //   console.log('All messages:', data.messages);
    // });

    // // Log real-time updates
    // socket.on('new_message', (data) => {
    //   console.log('New message:', data.message);
    // });


    socket.on('lab_products', (data) => {
      setProducts(data.products || []); // Update state with product data
    });
    
    // Cleanup on component unmount
    return () => {
      // socket.off('all_messages');
      // socket.off('new_message');
      socket.off('lab_products');
      socket.disconnect();
    };
  }, []);
*/