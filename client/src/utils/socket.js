// src/utils/socket.js
import { io } from 'socket.io-client'

const SOCKET_URL = "http://localhost:8080"
export const socket = io(SOCKET_URL, {
  autoConnect: false,
  withCredentials: true,
})
//WebSocket Manager