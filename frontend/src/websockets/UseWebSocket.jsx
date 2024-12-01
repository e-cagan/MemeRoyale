import { useState, useEffect } from "react";

function UseWebSocket(roomName, type, onMessageReceived) {
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/room/${roomName}/${type}/`);

    ws.onopen = () => {
      console.log("Connected to WebSocket");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessageReceived(data);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error", error);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    setSocket(ws);

    return () => {
      ws.close();
    };
  }, [roomName, type, onMessageReceived]);

  const sendMessage = (message) => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(message));
    }
  };

  return sendMessage;
}

export default UseWebSocket;
